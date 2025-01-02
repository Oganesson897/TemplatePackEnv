# TemplatePackEnv
Template workspace for modpacking Minecraft 1.12.2. Licensed under MIT, it is made for public use.  
The template is based on [Packwiz](https://packwiz.infra.link/).  
Install the [Packwiz application](https://github.com/packwiz/packwiz/actions/workflows/go.yml) to build the modpack locally.  

### Instructions:
0. Click use this template at the top.
1. Clone the repository that you have created with this template to your local machine.
2. Install the [Packwiz application](https://github.com/packwiz/packwiz/actions/workflows/go.yml)
3. Change modpack properties in [pack.toml](./pack.toml)
4. Move modpack files to here[^1].
5. Use `packwiz cf add <curseforge project name>` to add mod / `packwiz cf import <project url>` to import a curseforge modpack configuration.
6. Run `packwiz cf export` to export modpack file.

[^1]: e.g. `scripts` & `config`, No `mods`