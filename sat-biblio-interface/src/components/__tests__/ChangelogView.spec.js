import { describe, it, expect } from "vitest";
import ChangelogView from "@/components/ChangelogView.vue";

const render = (text) => ChangelogView.methods.renderMarkdown(text);

describe("ChangelogView.renderMarkdown", () => {
  it("convertit le Markdown en HTML", () => {
    expect(render("**gras**")).toContain("<strong>gras</strong>");
  });

  it("retire les scripts et les gestionnaires d'événements", () => {
    const html = render('<img src="x" onerror="alert(1)"><script>alert(2)</script> [lien](javascript:alert(3))');
    expect(html).not.toMatch(/onerror|<script|javascript:/i);
  });

  it("renvoie une chaîne vide sans texte", () => {
    expect(render("")).toBe("");
  });
});
