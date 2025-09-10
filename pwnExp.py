from pwn import *
import requests
file_name = "./pwn"
elf = ELF(file_name)


def exp(target, port=9999):
    io = remote(target, port)
    context(os='linux', arch='amd64', log_level='debug')
    #context.update(arch='i386',os='linux',log_level='debug')
    # context(os='linux', arch='amd64')
    #-------------- EXP -------------------#
    # 这里写攻击脚本



    flag = io.recvline()
    #-------------- END -------------------#
    io.interactive()
    io.close()
    return flag

def subbmitFlag(flag):
    """
    利用awd的api和token提交flag
    """
    token = "  " #在这里填写token
    inputFlag = f"https://ctf.bugku.com/pvp/submit.html?token={token}&flag={flag}"
    requests.get(inputFlag)


if __name__ == "__main__":
    with open('live.txt', 'r', encoding='utf-8') as target:
        for line in target:
            line = line.strip()
            flag = exp(line, 9999)
            subbmitFlag(flag)
