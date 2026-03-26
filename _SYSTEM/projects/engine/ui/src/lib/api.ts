export async function sendModerator(message: string): Promise<void> {
  await fetch('/moderator', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
}

export async function addQuestion(text: string): Promise<void> {
  await fetch('/questions/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
}

export async function fetchLedger(): Promise<string> {
  const res = await fetch('/ledger');
  return res.text();
}
