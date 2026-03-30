# BrainBread

BrainBread is a cooperative zombie survival mod for Valve's Half-Life (GoldSrc engine) where players fight together against hordes of zombies. Features include an arsenal of over 20 weapons, a gore system, AI-controlled military allies, and the risk of turning into a zombie yourself when bitten.

For more information visit the BrainBread website: https://ironoak.ch/BB/

## About This Repository

This repository contains the game assets, configuration files, and compiled binaries for BrainBread. For the source code, see [BrainBread](https://github.com/IronOak-Studios/BrainBread).

## Repository Structure

```
cl_dlls/        Compiled client-side DLL
dlls/           Compiled server-side game DLL
events/         Client-side weapon event scripts
gfx/            Graphics (skyboxes, key bindings, VGUI images)
help/           In-game help dialog configuration
manual/         HTML game manual and credits
maps/           Map descriptions, mission scripts, and configs
media/          Audio media (startup music)
models/         3D models (weapons, players, zombies, map objects)
partsys/        Particle system configuration
resource/       UI resources (localization, menus, loading screens)
sound/          Sound effects (weapons, zombies, ambience)
sprites/        2D sprites (HUD, weapon icons, effects, particles)
```

## Installation

1. Locate your Half-Life installation directory (e.g. `Half-Life/`)
2. Copy or clone this repository as a `brainbread` folder inside the Half-Life directory
3. Restart Steam -- BrainBread should appear in your game library

## License

This repository contains game assets and compiled binaries distributed under the following terms:

**Compiled game DLLs** (`cl_dlls/client.dll`, `dlls/bb.dll`) -- Built from source code based on the Half-Life SDK by Valve, Copyright (c) 1996-2002, Valve LLC. Subject to the Half-Life SDK License, which restricts use to non-commercial enhancements to products from Valve LLC. The source code is available separately.

**Original mod assets** (models, textures, sprites, sounds, maps, configuration files) -- Copyright (c) 2005-2026, IronOak Studios. Distributed for use with BrainBread. Commercial use is prohibited.

**Community-contributed maps** (`bb_uc1_*` series) -- Created by community members (credited in individual map description files). Included with permission.

This mod is provided for entertainment and educational purposes. Commercial use is prohibited.

## Trademarks

BrainBread is a trademark of IronOak Studios. Half-Life and Valve are trademarks of Valve Corporation.
