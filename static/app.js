const sourceText = document.querySelector("#source-text");
const translatedText = document.querySelector("#translated-text");
const sourceLabel = document.querySelector("#source-language");
const targetLabel = document.querySelector("#target-language");
const sourceOutputLabel = document.querySelector(".output-pane label");
const sourceInputLabel = document.querySelector(".pane:not(.output-pane) label");
const charCount = document.querySelector("#char-count");
const status = document.querySelector("#status");
const translateButton = document.querySelector("#translate");
const copyButton = document.querySelector("#copy");
const swapButton = document.querySelector("#swap");

let source = "en";
let target = "ko";

function updateLanguageLabels() {
  const names = { en: "English", ko: "Korean" };
  sourceLabel.textContent = names[source];
  targetLabel.textContent = names[target];
  sourceInputLabel.textContent = `${names[source]} text`;
  sourceOutputLabel.textContent = `${names[target]} translation`;
  sourceText.placeholder = `Enter ${names[source]} text to translate...`;
  translatedText.placeholder = `${names[target]} translation appears here`;
  document.documentElement.lang = source;
}

async function translate() {
  const text = sourceText.value.trim();
  if (!text) {
    translatedText.value = "";
    copyButton.disabled = true;
    status.textContent = "";
    return;
  }

  translateButton.disabled = true;
  status.textContent = "Translating...";
  try {
    const params = new URLSearchParams({ text, source, target });
    const response = await fetch(`/api/translate?${params}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Translation failed.");
    translatedText.value = data.translatedText;
    copyButton.disabled = false;
    status.textContent = "";
  } catch (error) {
    status.textContent = error.message;
  } finally {
    translateButton.disabled = false;
  }
}

sourceText.addEventListener("input", () => {
  charCount.textContent = `${sourceText.value.length} / 500`;
  if (!sourceText.value.trim()) {
    translatedText.value = "";
    copyButton.disabled = true;
    status.textContent = "";
  }
});

translateButton.addEventListener("click", translate);
sourceText.addEventListener("keydown", event => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") translate();
});

swapButton.addEventListener("click", () => {
  [source, target] = [target, source];
  const oldSource = sourceText.value;
  sourceText.value = translatedText.value;
  translatedText.value = oldSource;
  copyButton.disabled = !translatedText.value;
  charCount.textContent = `${sourceText.value.length} / 500`;
  updateLanguageLabels();
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(translatedText.value);
    status.textContent = "Copied";
  } catch {
    translatedText.select();
    document.execCommand("copy");
    status.textContent = "Copied";
  }
});

updateLanguageLabels();
