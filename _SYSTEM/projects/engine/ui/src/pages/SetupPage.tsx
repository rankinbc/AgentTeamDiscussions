import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchBriefs, fetchAgents, fetchTeams, startSession } from '../lib/api';
import type { BriefInfo, AgentInfo, TeamInfo } from '../lib/api';

export default function SetupPage() {
  const navigate = useNavigate();
  const [topic, setTopic] = useState('');
  const [briefs, setBriefs] = useState<BriefInfo[]>([]);
  const [allAgents, setAllAgents] = useState<AgentInfo[]>([]);
  const [teams, setTeams] = useState<TeamInfo[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);
  const [selectedBrief, setSelectedBrief] = useState<string | null>(null);
  const [selectedAgents, setSelectedAgents] = useState<Set<string>>(new Set());
  const [launching, setLaunching] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchBriefs().then(setBriefs).catch(() => {});
    fetchAgents().then(setAllAgents).catch(() => {});
    fetchTeams().then(t => {
      setTeams(t);
      // Select first team by default
      if (t.length > 0) {
        setSelectedTeam(t[0].name);
        setSelectedAgents(new Set(t[0].agents));
      }
    }).catch(() => {});
  }, []);

  // Agents visible based on team selection (or all if "custom")
  const visibleAgents = selectedTeam === '_custom'
    ? allAgents
    : allAgents.filter(a => {
        const team = teams.find(t => t.name === selectedTeam);
        return team ? team.agents.includes(a.key) : true;
      });

  const selectTeam = (teamName: string) => {
    setSelectedTeam(teamName);
    if (teamName === '_custom') {
      // Keep current selection when switching to custom
      return;
    }
    const team = teams.find(t => t.name === teamName);
    if (team) {
      setSelectedAgents(new Set(team.agents));
    }
  };

  const selectBrief = (b: BriefInfo) => {
    if (selectedBrief === b.filename) {
      setSelectedBrief(null);
      setTopic('');
    } else {
      setSelectedBrief(b.filename);
      setTopic(b.content);
    }
  };

  const handleTopicChange = (val: string) => {
    setTopic(val);
    setSelectedBrief(null);
  };

  const toggleAgent = (key: string) => {
    setSelectedTeam('_custom');
    setSelectedAgents(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  const canStart = topic.trim().length > 0 && selectedAgents.size >= 2;

  const handleStart = async () => {
    if (!canStart || launching) return;
    setLaunching(true);
    setError('');
    try {
      const team = selectedTeam !== '_custom' ? selectedTeam ?? undefined : undefined;
      await startSession(topic, Array.from(selectedAgents), team);
      navigate('/session');
    } catch (e: any) {
      setError(e.message || 'Failed to start session');
      setLaunching(false);
    }
  };

  return (
    <div className="setup-page">
      <header className="setup-hdr">
        <div className="hdr-logo">ATD <span>// SETUP</span></div>
      </header>

      <div className="setup-content">
        {/* Topic */}
        <section className="setup-section">
          <h2 className="setup-label">What should the agents discuss?</h2>
          <textarea
            className="setup-topic"
            value={topic}
            onChange={e => handleTopicChange(e.target.value)}
            placeholder="Describe the topic, paste questions, or select a brief below..."
            rows={6}
          />
        </section>

        {/* Briefs */}
        {briefs.length > 0 && (
          <section className="setup-section">
            <h2 className="setup-label">Or start from a brief</h2>
            <div className="brief-row">
              {briefs.map(b => (
                <button
                  key={b.filename}
                  className={`brief-card ${selectedBrief === b.filename ? 'selected' : ''}`}
                  onClick={() => selectBrief(b)}
                >
                  {b.name}
                </button>
              ))}
            </div>
          </section>
        )}

        {/* Team selector */}
        {teams.length > 0 && (
          <section className="setup-section">
            <h2 className="setup-label">Team</h2>
            <div className="brief-row">
              {teams.map(t => (
                <button
                  key={t.name}
                  className={`brief-card ${selectedTeam === t.name ? 'selected' : ''}`}
                  onClick={() => selectTeam(t.name)}
                >
                  {t.displayName} <span className="team-count">({t.agentCount})</span>
                </button>
              ))}
              <button
                className={`brief-card ${selectedTeam === '_custom' ? 'selected' : ''}`}
                onClick={() => selectTeam('_custom')}
              >
                Custom mix
              </button>
            </div>
          </section>
        )}

        {/* Agents */}
        <section className="setup-section">
          <h2 className="setup-label">
            Agents
            {selectedTeam && selectedTeam !== '_custom' && (
              <span className="setup-label-hint"> — {selectedAgents.size} selected</span>
            )}
            {selectedTeam === '_custom' && (
              <span className="setup-label-hint"> — {selectedAgents.size} selected from all teams</span>
            )}
          </h2>
          <div className="agent-grid">
            {visibleAgents.map(a => {
              const on = selectedAgents.has(a.key);
              return (
                <div
                  key={a.key}
                  className={`setup-agent-card ${on ? 'selected' : 'dimmed'}`}
                  onClick={() => toggleAgent(a.key)}
                >
                  <div className="sac-check">{on ? '\u2713' : ''}</div>
                  <div className="sac-name">{a.name}</div>
                  <div className="sac-role">{a.role}</div>
                  {Object.entries(a.traits).map(([name, val]) => (
                    <div key={name} className="trait-row">
                      <span className="trait-lbl">{name}</span>
                      <div className="trait-bar">
                        <div className="trait-fill" style={{ width: `${val * 100}%`, background: on ? 'var(--blue)' : 'var(--dim)' }} />
                      </div>
                      <span className="trait-val">{val.toFixed(1)}</span>
                    </div>
                  ))}
                  {a.drives.length > 0 && (
                    <div className="sac-drives">
                      {a.drives.slice(0, 2).map((d, i) => (
                        <div key={i} className="sac-drive">{d}</div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Footer */}
        <div className="setup-footer">
          <a className="setup-link dim" href="#">+ Create new agent</a>
          {error && <span className="setup-error">{error}</span>}
          <button
            className={`setup-start ${canStart ? '' : 'disabled'}`}
            onClick={handleStart}
            disabled={!canStart || launching}
          >
            {launching ? 'Starting...' : 'Start Discussion'}
          </button>
        </div>
      </div>
    </div>
  );
}
