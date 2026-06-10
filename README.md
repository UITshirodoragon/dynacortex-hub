# DynaCortex | MMLab UIT

**Project Hub for Dynamic Cortex in Embodied AI and Robotics at MMLab UIT**

DynaCortex là nhóm các dự án nghiên cứu và thử nghiệm về Trí tuệ nhân tạo hiện thân và Robot (Embodied AI & Robotics), được thực hiện tại Phòng thí nghiệm Đa phương tiện (MMLab) thuộc Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT). Chuỗi các dự án này tập trung phát triển hệ thống nhận thức thông minh (Cortex) kết hợp chặt chẽ với động lực học chuyển động (Dynamics) của robot.

## Documentation Stack

- Quarto
- QMD / Markdown
- GitHub Pages
- GitHub Actions
- Zotero / BibTeX for references

## Main Sections

| Section | Purpose |
|---|---|
| `examples/` | Minimal examples for QMD syntax |
| `01-system-foundations/` | Mathematical, technical, theoretical, and system-level foundations |
| `02-implementation/` | Setup, code, runtime, deployment, and default configuration |
| `03-experiments/` | Experiments, logs, data, and results |
| `04-reference/` | Standard references, commands, tables, and configuration schemas |
| `05-literature/` | Paper notes and literature review |
| `06-reports/` | Complete technical reports |
| `07-inbox/` | Quick notes and unprocessed ideas |
| `08-notes/` | Learning notes |
| `09-troubleshooting/` | Issues, causes, checks, and fixes |

## Local Preview

```bash
quarto preview
```

## Render

```bash
quarto render
```

## Deploy

This repository includes a GitHub Actions workflow at `.github/workflows/publish.yml`. Push to `main`, then configure GitHub Pages to deploy from the `gh-pages` branch.

```bash
git add .
git commit -m "Update DynaCortex Hub"
git push
```
