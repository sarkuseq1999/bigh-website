// Puts each sentence of a short line on a line of its own ("What our name stands for." /
// "What our work is for."), so a narrow column never breaks it mid-thought. Languages without
// ". " between sentences simply show the line as it is.
export function Sentences({ text }: { text: string }) {
  return text.split(/(?<=[.!?])\s+/).map((sentence) => (
    <span key={sentence} style={{ display: "block" }}>
      {sentence}
    </span>
  ));
}
