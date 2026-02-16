import os
import tempfile
import pytest
from utils.cryptography import padding, unpad, encryptAES, encrypt_hybrid, decrypt_hybrid, decrypt_hybrid_qvault
from utils.qvaults import QVaultFormat
from utils.logging import log_message
import cli
import main

# TODO: SEPARATE ALL TESTS BY MODULES

def test_padding_and_unpad():
    data = b"abc"
    padded = padding(data)
    assert len(padded) % 16 == 0
    assert unpad(padded) == data

@pytest.mark.parametrize("data", [b"", b"a", b"1234567890abcdef"])
def test_padding_unpad_various(data):
    padded = padding(data)
    assert unpad(padded) == data


def test_encryptAES_and_decrypt():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"test1234")
        fname = f.name
    aes_key = os.urandom(32)
    ciphertext, iv = encryptAES(fname, aes_key)

    from Crypto.Cipher import AES as _AES
    cipher = _AES.new(aes_key, _AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))
    assert plaintext == b"test1234"
    os.unlink(fname)


def test_encrypt_hybrid_and_decrypt_hybrid_qvault():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hybrid test")
        fname = f.name
    qvault_file = fname + ".qvault"
    encrypt_hybrid(fname, qvault_file)
    key_file = qvault_file.replace('.qvault', '.key')
    out_file = fname + "_decrypted"
    decrypt_hybrid_qvault(qvault_file, out_file, key_file)

    with open(out_file, 'rb') as f:
        assert f.read() == b"hybrid test"
    for f in [fname, qvault_file, key_file, out_file+".txt", out_file]:
        if os.path.exists(f):
            os.unlink(f)


def test_decrypt_hybrid_legacy():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"legacy test")
        fname = f.name
    out = fname + ".enc"

    from utils.cryptography import encrypt_hybrid
    encrypt_hybrid(fname, out)

    assert os.path.exists(out)
    assert os.path.exists(out+".iv")
    assert os.path.exists(out+".kem")
    assert os.path.exists(out+".pub")
    assert os.path.exists(out+".sec")

    decrypt_hybrid(out, out+"_dec", out+".sec", out+".kem", out+".iv")
    with open(out+"_dec", 'rb') as f:
        assert f.read() == b"legacy test"
    for f in [fname, out, out+".iv", out+".kem", out+".pub", out+".sec", out+"_dec"]:
        if os.path.exists(f):
            os.unlink(f)


def test_create_header_and_pack_unpack():
    data = b"data"
    iv = b"1"*16
    kem = b"2"*32
    pub = b"3"*32
    ext = ".txt"
    with tempfile.NamedTemporaryFile(delete=False) as f:
        out = f.name + ".qvault"
    QVaultFormat.pack_qvault(data, iv, kem, pub, out, ext)

    d, i, k, p, e = QVaultFormat.unpack_qvault(out)
    assert d == data
    assert i == iv
    assert k == kem
    assert p == pub
    assert e == ext
    os.unlink(out)


def test_is_qvault_file_and_get_info():
    data = b"d"
    iv = b"i"*16
    kem = b"k"*32
    pub = b"p"*32
    ext = ".bin"
    with tempfile.NamedTemporaryFile(delete=False) as f:
        out = f.name + ".qvault"
    QVaultFormat.pack_qvault(data, iv, kem, pub, out, ext)
    assert QVaultFormat.is_qvault_file(out)
    info = QVaultFormat.get_qvault_info(out)
    assert info is not None
    assert info['original_extension'] == ext
    os.unlink(out)

def test_log_message(tmp_path):
    log_message("pytest test log", "pytest", "info")
    logs = os.listdir("logs")

    assert any(f.endswith(".txt") for f in logs)

def test_commands():
    cmds = cli.commands()
    assert "encrypt" in cmds and "decrypt" in cmds

def test_initCli_help_and_version(capsys):
    cli.initCli(["-h"])
    out = capsys.readouterr().out
    assert "List of commands" in out
    cli.initCli(["-v"])
    out = capsys.readouterr().out
    assert "Version" in out

def test_initCli_invalid(capsys):
    cli.initCli(["--invalid"])
    out = capsys.readouterr().out
    assert "List of commands" in out

def test_main_runs(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "-h"])
    main.main()
