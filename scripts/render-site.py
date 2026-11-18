#!/usr/bin/env python3
"""Render generated sections in index.html from data/projects.json.

Usage:
    python3 scripts/render-site.py

This keeps the site as a single static HTML file (no runtime fetch),
so the page can be updated from JSON without rewriting the layout.
Do not put prices, checkout, or payment links into the JSON: the
cyberfrank.is-a.dev domain is bound by is-a.dev terms that prohibit
commercial / for-profit use.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "projects.json"
HTML = ROOT / "index.html"
SKILLS_BEGIN = "<!-- BEGIN:GENERATED:skills -->"
SKILLS_END = "<!-- END:GENERATED:skills -->"
PROJECT_BEGIN = "<!-- BEGIN:GENERATED:contract-project -->"
PROJECT_END = "<!-- END:GENERATED:contract-project -->"


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def skill_card(skill: dict) -> str:
    install = skill.get("install") or {}
    url = install.get("url")
    howto = install.get("howto") or ""
    query = install.get("query") or skill["name"]
    if url:
        action = f'<a class="skill-action" href="{esc(url)}">打开技能页</a>'
    else:
        fallback = howto or f"在 WorkBuddy 技能市场搜索「{query}」安装。"
        action = f'<p class="skill-howto">{esc(fallback)}</p>'
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in skill.get("tags") or [])
    platform = esc(skill.get("platform") or "Skill")
    status = esc(skill.get("status") or "已发布")
    name = esc(skill["name"])
    summary = esc(skill.get("summary") or "")
    return (
        '          <article class="project project-third reveal">\n'
        f'            <div class="project-head"><span class="project-type">{platform}</span>'
        f'<span class="status">{status}</span></div>\n'
        f"            <h3>{name}</h3>\n"
        f'            <p class="project-desc">{summary}</p>\n'
        f'            <div class="project-tags">{tags}</div>\n'
        f"            {action}\n"
        "          </article>"
    )


def contract_card(project: dict) -> str:
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in project.get("tags") or [])
    metrics = "".join(
        f'<div><b>{esc(m["value"])}</b><span>{esc(m["label"])}</span></div>'
        for m in project.get("metrics") or []
    )
    status_class = esc(project.get("status_class") or "prototype")
    extra = ""
    if project.get("url"):
        extra = (
            f'<p class="skill-howto"><a class="skill-action" href="{esc(project["url"])}">'
            "了解项目</a></p>"
        )
    ptype = esc(project.get("type") or "LegalTech")
    status = esc(project.get("status") or "进行中")
    name = esc(project["name"])
    summary = esc(project.get("summary") or "")
    return (
        '          <article class="project project-small reveal">\n'
        f'            <div class="project-head"><span class="project-type">{ptype}</span>'
        f'<span class="status {status_class}">{status}</span></div>\n'
        f"            <h3>{name}</h3>\n"
        f'            <p class="project-desc">{summary}</p>\n'
        f'            <div class="project-tags">{tags}</div>\n'
        f'            <div class="project-metrics">{metrics}</div>\n'
        f"            {extra}\n"
        "          </article>"
    )


def replace_block(html: str, begin: str, end: str, inner: str) -> str:
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if not pattern.search(html):
        raise SystemExit(f"Missing markers {begin} ... {end} in index.html")
    return pattern.sub(begin + "\n" + inner.rstrip() + "\n          " + end, html)


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    skills_inner = "\n".join(skill_card(s) for s in payload.get("skills") or [])
    projects = payload.get("projects") or []
    contract = next((p for p in projects if p.get("id") == "yifang-hetong-tijian"), None)
    html = HTML.read_text(encoding="utf-8")
    html = replace_block(html, SKILLS_BEGIN, SKILLS_END, skills_inner)
    if contract:
        html = replace_block(html, PROJECT_BEGIN, PROJECT_END, contract_card(contract))
    HTML.write_text(html, encoding="utf-8")
    print(f"Rendered {len(payload.get('skills') or [])} skills into {HTML}")


if __name__ == "__main__":
    main()
