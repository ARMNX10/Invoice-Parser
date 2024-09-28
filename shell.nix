{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell rec {
  buildInputs = with pkgs; [
    poppler_utils
  ];
  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  shellHook = ''
    python -m venv env
    source ./env/bin/activate
  '';
}
