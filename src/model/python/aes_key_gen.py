#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#=======================================================================
#
# aes_key_gen.py
# -------------
# Simple, pure Python test model of the AES key generation.
#
#
# Author: Joachim Strömbergson
# Copyright (c) 2014, Secworks Sweden AB
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the following 
# conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer. 
# 
# 2. Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in 
#    the documentation and/or other materials provided with the 
#    distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#=======================================================================

#-------------------------------------------------------------------
# Python module imports.
#-------------------------------------------------------------------
import sys


#-------------------------------------------------------------------
# Constants.
#-------------------------------------------------------------------
VERBOSE = True

AES_128_ROUNDS = 10
AES_192_ROUNDS = 12
AES_256_ROUNDS = 14


sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
        0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
        0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
        0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
        0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
        0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
        0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
        0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
        0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
        0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
        0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
        0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
        0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
        0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
        0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
        0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]


#-------------------------------------------------------------------
# substw()
#
# Returns a 32-bit word in which each of the bytes in the
# given 32-bit word has been used as lookup into the AES S-box.
#-------------------------------------------------------------------
def substw(w):
    b0 = w >> 24
    b1 = w >> 16 & 0xff
    b2 = w >> 8 & 0xff
    b3 = w & 0xff

    s0 = sbox[b0]
    s1 = sbox[b1]
    s2 = sbox[b2]
    s3 = sbox[b3]

    return (s0 << 24) + (s1 << 16) + (s2 << 8) + s3


#-------------------------------------------------------------------
# rol8()
#
# Rotate the given 32 bit word 8 bits left.
#-------------------------------------------------------------------
def rol8(w):
    return ((w << 8) | (w >> 24)) & 0xffffffff


#-------------------------------------------------------------------
# key_gen()
#
# The actual key generation.
#-------------------------------------------------------------------
def key_gen(key):
    if VERBOSE:
        print("key length: %d" % len(key))

    round_keys = []
    round_keys.append(key)
    rcon = 0x8d

    for i in range(1, AES_128_ROUNDS + 1):
        rcon = ((rcon << 1) ^ (0x11b & - (rcon >> 7))) & 0xff
        (prev_x0, prev_x1, prev_x2, prev_x3) = round_keys[(i-1)]
        tmp = substw(rol8(prev_x3)) ^ (rcon << 24)
        x0 = prev_x0 ^ tmp
        x1 = prev_x1 ^ x0
        x2 = prev_x2 ^ x1
        x3 = prev_x3 ^ x2
        round_keys.append((x0, x1, x2, x3))
        if VERBOSE:
            print("rcon = 0x%02x, rconw = 0x%08x" % (rcon, rcon << 24))

    if VERBOSE:
        for i in range(AES_128_ROUNDS + 1):
            (x0, x1, x2, x3) = round_keys[i]
            print("Round %02d: x0 = 0x%08x, x1 = 0x%08x, x2 = 0x%08x, x3 = 0x%08x"\
                  % (i, x0, x1, x2, x3))
    return round_keys


#-------------------------------------------------------------------
# test_keys()
#
# Generate round keys for a given key and compare them to
# the given expected round keys.
#-------------------------------------------------------------------
def test_keys(key, expected):
    generated = key_gen(key)
    print("Expected number of round keys: %d" % len(expected))
    print("Got number of round keys:      %d" % len(generated))


#-------------------------------------------------------------------
# main()
#
# If executed tests the ChaCha class using known test vectors.
#-------------------------------------------------------------------
def main():
    print("Testing the AES key generation")
    print("==============================")
    print
    test_key0 = (0x00000000, 0x00000000, 0x00000000, 0x00000000)
    expected0 = ((0x00000000, 0x00000000, 0x00000000, 0x00000000),
                 (0x62636363, 0x62636363, 0x62636363, 0x62636363),
                 (0x9b9898c9, 0xf9fbfbaa, 0x9b9898c9, 0xf9fbfbaa),
                 (0x90973450, 0x696ccffa, 0xf2f45733, 0x0b0fac99),
                 (0xee06da7b, 0x876a1581, 0x759e42b2, 0x7e91ee2b),
                 (0x7f2e2b88, 0xf8443e09, 0x8dda7cbb, 0xf34b9290),
                 (0xec614b85, 0x1425758c, 0x99ff0937, 0x6ab49ba7),
                 (0x21751787, 0x3550620b, 0xacaf6b3c, 0xc61bf09b),
                 (0x0ef90333, 0x3ba96138, 0x97060a04, 0x511dfa9f),
                 (0xb1d4d8e2, 0x8a7db9da, 0x1d7bb3de, 0x4c664941),
                 (0xb4ef5bcb, 0x3e92e211, 0x23e951cf, 0x6f8f188e))

    test_key1 = (0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff)
    expected1 = ((0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff),
                 (0xe8e9e9e9, 0x17161616, 0xe8e9e9e9, 0x17161616),
                 (0xadaeae19, 0xbab8b80f, 0x525151e6, 0x454747f0),
                 (0x090e2277, 0xb3b69a78, 0xe1e7cb9e, 0xa4a08c6e),
                 (0xe16abd3e, 0x52dc2746, 0xb33becd8, 0x179b60b6),
                 (0xe5baf3ce, 0xb766d488, 0x045d3850, 0x13c658e6),
                 (0x71d07db3, 0xc6b6a93b, 0xc2eb916b, 0xd12dc98d),
                 (0xe90d208d, 0x2fbb89b6, 0xed5018dd, 0x3c7dd150),
                 (0x96337366, 0xb988fad0, 0x54d8e20d, 0x68a5335d),
                 (0x8bf03f23, 0x3278c5f3, 0x66a027fe, 0x0e0514a3),
                 (0xd60a3588, 0xe472f07b, 0x82d2d785, 0x8cd7c326))

    test_key2 = (0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f)
    expected2 = ((0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f),
                 (0xd6aa74fd, 0xd2af72fa, 0xdaa678f1, 0xd6ab76fe),
                 (0xb692cf0b, 0x643dbdf1, 0xbe9bc500, 0x6830b3fe),
                 (0xb6ff744e, 0xd2c2c9bf, 0x6c590cbf, 0x0469bf41),
                 (0x47f7f7bc, 0x95353e03, 0xf96c32bc, 0xfd058dfd),
                 (0x3caaa3e8, 0xa99f9deb, 0x50f3af57, 0xadf622aa),
                 (0x5e390f7d, 0xf7a69296, 0xa7553dc1, 0x0aa31f6b),
                 (0x14f9701a, 0xe35fe28c, 0x440adf4d, 0x4ea9c026),
                 (0x47438735, 0xa41c65b9, 0xe016baf4, 0xaebf7ad2),
                 (0x549932d1, 0xf0855768, 0x1093ed9c, 0xbe2c974e),
                 (0x13111d7f, 0xe3944a17, 0xf307a78b, 0x4d2b30c5))

    test_key3 = (0x6920e299, 0xa5202a6d, 0x656e6368, 0x69746f2a)
    expected3 = ((0x6920e299, 0xa5202a6d, 0x656e6368, 0x69746f2a),
                 (0xfa880760, 0x5fa82d0d, 0x3ac64e65, 0x53b2214f),
                 (0xcf75838d, 0x90ddae80, 0xaa1be0e5, 0xf9a9c1aa),
                 (0x180d2f14, 0x88d08194, 0x22cb6171, 0xdb62a0db),
                 (0xbaed96ad, 0x323d1739, 0x10f67648, 0xcb94d693),
                 (0x881b4ab2, 0xba265d8b, 0xaad02bc3, 0x6144fd50),
                 (0xb34f195d, 0x096944d6, 0xa3b96f15, 0xc2fd9245),
                 (0xa7007778, 0xae6933ae, 0x0dd05cbb, 0xcf2dcefe),
                 (0xff8bccf2, 0x51e2ff5c, 0x5c32a3e7, 0x931f6d19),
                 (0x24b7182e, 0x7555e772, 0x29674495, 0xba78298c),
                 (0xae127cda, 0xdb479ba8, 0xf220df3d, 0x4858f6b1))


    test_keys(test_key0, expected0)
    test_keys(test_key1, expected1)
    test_keys(test_key2, expected2)
    test_keys(test_key3, expected3)


#-------------------------------------------------------------------
# __name__
# Python thingy which allows the file to be run standalone as
# well as parsed from within a Python interpreter.
#-------------------------------------------------------------------
if __name__=="__main__": 
    # Run the main function.
    sys.exit(main())

#=======================================================================
# EOF aes_key_gen.py
#=======================================================================
