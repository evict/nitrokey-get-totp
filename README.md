## Usage
Easily obtain Nitrokey TOTP codes.

- Install `libnitrokey`, `libnitrokey-dev` (header package), `dmenu` and `xclip` for your distribution.
- Install the required Python library.
- Make sure the library and header paths are correctly set in the `get_library` function.

Place the `otpmenu` and `nitro_get_otp.py` in the same directory, preferably in your PATH, i.e. `${HOME}/bin`.

Run `otpmenu`.

## Credits
This code is based on the [python_bindings_example](https://github.com/Nitrokey/libnitrokey/blob/master/python_bindings_example.py) from the Nitrokey project.
