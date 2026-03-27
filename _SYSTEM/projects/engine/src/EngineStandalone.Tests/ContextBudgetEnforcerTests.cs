using EngineStandalone.Telemetry;
using Xunit;

namespace EngineStandalone.Tests;

public class ContextBudgetEnforcerTests
{
    private static ContextSection MakeSection(string name, int chars, bool isProtected = false)
    {
        var content = new string('x', chars);
        return new ContextSection(name, content, isProtected);
    }

    private static ContextSnapshot MakeSnapshot(List<ContextSection> sections, int budgetTokens = 4000)
    {
        return new ContextSnapshot
        {
            AgentKey = "test_agent",
            RoundName = "propose",
            QuestionNumber = 1,
            BudgetTokens = budgetTokens,
            Sections = sections
        };
    }

    [Fact]
    public void Diagnose_OverBudget_ReturnsTrue()
    {
        var enforcer = new ContextBudgetEnforcer(maxPayloadTokens: 100);

        // 500 chars = 125 tokens (over 100 budget)
        var snapshot = MakeSnapshot([MakeSection("prior_rounds", 500)], budgetTokens: 100);
        var diagnosis = enforcer.Diagnose(snapshot);

        Assert.True(diagnosis.IsOverBudget);
        Assert.True(diagnosis.ExcessTokens > 0);
    }

    [Fact]
    public void Diagnose_UnderBudget_ReturnsFalse()
    {
        var enforcer = new ContextBudgetEnforcer(maxPayloadTokens: 4000);

        // 100 chars = 25 tokens (well under 4000 budget)
        var snapshot = MakeSnapshot([MakeSection("prior_rounds", 100)], budgetTokens: 4000);
        var diagnosis = enforcer.Diagnose(snapshot);

        Assert.False(diagnosis.IsOverBudget);
        Assert.Equal(0, diagnosis.ExcessTokens);
    }

    [Fact]
    public void Diagnose_Imbalanced_FlagsSection()
    {
        var enforcer = new ContextBudgetEnforcer(maxPayloadTokens: 4000, imbalanceThreshold: 0.60);

        // prior_rounds = 7000 chars = 1750 tokens (70% of cuttable total)
        // decisions = 1000 chars = 250 tokens (10%)
        // question = 2000 chars = 500 tokens (protected — excluded from cuttable calculation)
        var sections = new List<ContextSection>
        {
            MakeSection("prior_rounds", 7000),
            MakeSection("decisions", 1000),
            MakeSection("question", 2000, isProtected: true)
        };
        var snapshot = MakeSnapshot(sections);
        var diagnosis = enforcer.Diagnose(snapshot);

        Assert.True(diagnosis.IsImbalanced);
        Assert.Equal("prior_rounds", diagnosis.OffendingSection);
    }

    [Fact]
    public void Diagnose_Balanced_IsImbalancedFalse()
    {
        var enforcer = new ContextBudgetEnforcer(maxPayloadTokens: 4000, imbalanceThreshold: 0.60);

        // Each cuttable section = 33% — none exceed 60%
        var sections = new List<ContextSection>
        {
            MakeSection("prior_rounds", 1000),
            MakeSection("prior_specs", 1000),
            MakeSection("decisions", 1000)
        };
        var snapshot = MakeSnapshot(sections);
        var diagnosis = enforcer.Diagnose(snapshot);

        Assert.False(diagnosis.IsImbalanced);
        Assert.Null(diagnosis.OffendingSection);
    }

    [Fact]
    public void Enforce_OverBudget_BringsUnderCeiling()
    {
        var maxTokens = 200;
        var enforcer = new ContextBudgetEnforcer(maxPayloadTokens: maxTokens);

        // 4000 chars = 1000 tokens — way over 200
        var sections = new List<ContextSection>
        {
            MakeSection("prior_rounds", 4000),
            MakeSection("question", 200, isProtected: true)
        };
        var snapshot = MakeSnapshot(sections, budgetTokens: maxTokens);
        var diagnosis = enforcer.Diagnose(snapshot);

        var (result, actions) = enforcer.Enforce(sections, diagnosis);
        var totalTokens = result.Sum(s => s.Tokens);

        Assert.True(totalTokens <= maxTokens, $"Expected ≤{maxTokens} tokens, got {totalTokens}");
        Assert.NotEmpty(actions);
    }

    [Fact]
    public void Enforce_ProtectedSectionsUntouched()
    {
        var enforcer = new ContextBudgetEnforcer(maxPayloadTokens: 50);

        var protectedContent = new string('p', 500);
        var sections = new List<ContextSection>
        {
            new ContextSection("prior_rounds", new string('x', 2000)),
            new ContextSection("question", protectedContent, IsProtected: true),
            new ContextSection("round_instruction", new string('y', 500), IsProtected: true)
        };
        var snapshot = MakeSnapshot(sections, budgetTokens: 50);
        var diagnosis = enforcer.Diagnose(snapshot);

        var (result, _) = enforcer.Enforce(sections, diagnosis);

        var questionSection = result.First(s => s.Name == "question");
        var instructionSection = result.First(s => s.Name == "round_instruction");

        Assert.Equal(protectedContent, questionSection.Content);
        Assert.Equal(500, instructionSection.Chars);
    }

    [Fact]
    public void Enforce_CutOrder_PriorRoundsFirst()
    {
        var enforcer = new ContextBudgetEnforcer(maxPayloadTokens: 300);

        // prior_rounds = 800 chars = 200 tokens
        // prior_specs = 800 chars = 200 tokens
        // Total = 400 tokens, budget = 300 — needs one trim
        var sections = new List<ContextSection>
        {
            MakeSection("prior_rounds", 800),
            MakeSection("prior_specs", 800)
        };
        var snapshot = MakeSnapshot(sections, budgetTokens: 300);
        var diagnosis = enforcer.Diagnose(snapshot);

        var (result, actions) = enforcer.Enforce(sections, diagnosis);

        // prior_rounds should be trimmed (it's first in cut priority)
        var priorRounds = result.First(s => s.Name == "prior_rounds");
        var priorSpecs = result.First(s => s.Name == "prior_specs");

        // After trimming prior_rounds to 50%, we should be under budget
        // prior_rounds was 200 tokens → trimmed to ~100; prior_specs stays at 200 → total ~300 ≤ budget
        Assert.True(priorRounds.Chars < 800, "prior_rounds should have been trimmed first");
        Assert.True(actions.Any(a => a.Contains("prior_rounds")));
    }

    [Fact]
    public void Enforce_RescueActions_PopulatedCorrectly()
    {
        var enforcer = new ContextBudgetEnforcer(maxPayloadTokens: 100);

        var sections = new List<ContextSection>
        {
            MakeSection("prior_rounds", 2000),
            MakeSection("question", 100, isProtected: true)
        };
        var snapshot = MakeSnapshot(sections, budgetTokens: 100);
        var diagnosis = enforcer.Diagnose(snapshot);

        var (_, actions) = enforcer.Enforce(sections, diagnosis);

        Assert.NotEmpty(actions);
        Assert.Contains("prior_rounds", actions[0]);
    }
}
