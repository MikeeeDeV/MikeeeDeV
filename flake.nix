{
  description = "Hermetic, deterministic profile generator environment for Mohamed Ayman (@MikeeeDeV)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          pyyaml
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          name = "mikeeedev-profile-devshell";
          buildInputs = [
            pythonEnv
            pkgs.git
            pkgs.gh
            pkgs.gnumake
          ];

          shellHook = ''
            echo "❄️ Entering hermetic Nix shell for MikeeeDeV profile engine"
            echo "Python: $(python3 --version)"
            echo "Available commands: make build | make test | make preview"
          '';
        };

        packages.default = pkgs.stdenv.mkDerivation {
          pname = "mikeeedev-profile-artifacts";
          version = "1.0.0";
          src = ./.;

          buildInputs = [ pythonEnv ];

          buildPhase = ''
            export HOME=$TMPDIR
            python3 scripts/generate_neofetch.py || true
            python3 scripts/generate_cipher_banner.py
            python3 scripts/generate_now_building.py
            python3 scripts/generate_contributions.py
            python3 scripts/generate_pins.py
            python3 scripts/generate_hero_typing.py
            python3 scripts/generate_visitor_ledger.py
            python3 scripts/generate_mcp_card.py
          '';

          installPhase = ''
            mkdir -p $out/assets
            cp -r assets/* $out/assets/
            cp README.md $out/
          '';
        };
      }
    );
}
