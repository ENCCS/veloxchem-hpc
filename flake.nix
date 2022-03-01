{
  description = "veloxchem-hpc";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pypi-deps-db = {
      url = "github:DavHau/pypi-deps-db/a8ea7f774b76d3b61237c0bc20c97629a2248462";
      flake = false;
    };
    mach-nix = {
      url = "mach-nix/3.4.0";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
      inputs.pypi-deps-db.follows = "pypi-deps-db";
    }; 
  };

  outputs = { self, nixpkgs, flake-utils, mach-nix, pypi-deps-db }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = mach-nix.lib."${system}".mkPython {
          requirements = builtins.readFile ./requirements.txt + ''
            # additional dependencies for local work
            jupyterlab
            pandas
          '';
        };
      in
      {
        devShell = pkgs.mkShell {
          nativeBuildInputs = [ ];
          buildInputs = [
            pythonEnv
          ];
        };
      });
}
