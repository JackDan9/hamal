# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg
import passlib.utils

from hamal.conf import utils


max_password_length = cfg.IntOpt(
    'max_password_length',
    default=4096,
    max=passlib.utils.MAX_PASSWORD_SIZE,
    help=utils.fmt("""
Maximum allowed length for user passwords. Decrease this value to improve
performance. Changing this value does not effect existing passwords.
"""))

password_hash_algorithm = cfg.StrOpt(
    'password_hash_algorithm',
    choices=['bcrypt', 'scrypt', 'pbkdf2_sha512'],
    default='bcrypt',
    help=utils.fmt("""
The password hashing algorithm to use for passwords stored within hamal.    
"""))

password_hash_rounds = cfg.IntOpt(
    'password_hash_rounds',
    help=utils.fmt("""
This option represents a trade off between security and performance. Higher
values lead to slower performance, but higher security. Changing this option
will only affect newly created passwords as existing password hashes already
have a fixed number of rounds applied, so it is safe to tune this option in a
running cluster.

The default for bcrypt is 12, must be between 4 and 31, inclusive.

The default for scrypt is 16, must be within `range(1,32)`.

The default for pbkdf_sha512 is 60000, must be within `range(1,1<32)`

WARNING: If using scrypt, increasing this value increases BOTH time AND
memory requirements to hash a password.
"""))

salt_bytesize = cfg.IntOpt(
    'salt_bytesize',
    min=0,
    max=96,
    help=utils.fmt("""
Number of bytes to use in scrypt and pbkfd2_sha512 hashing salt.

Default for scrypt is 16 bytes.
Default for pbkfd2_sha512 is 16 bytes.

Limited to a maximum of 96 bytes due to the size of the column used to store
password hashes.
"""))

scrypt_block_size = cfg.IntOpt(
    'scrypt_block_size',
    help=utils.fmt("""
Optional block size to pass to scrypt hash function (the `r` parameter).
Useful for tuning scrypt to optimal performance for your CPU architecture.
This option is only used when the `password_hash_algorithm` option is set
to `scrypt`. Defaults to 8.
"""))

scrypt_paralellism = cfg.IntOpt(
    'scrypt_parallelism',
    help=utils.fmt("""
Optional parallelism to pass to scrypt hash function (the `p` parameter).
This option is only used when the `password_hash_algorithm` option is set 
to `scrypt`. Defaults to 1.
"""))

GROUP_NAME = __name__.split('.')[-1]

ALL_OPTS = [
    max_password_length,
    password_hash_algorithm,
    password_hash_rounds,
    scrypt_block_size,
    scrypt_paralellism,
    salt_bytesize
]


def register_opts(conf):
    conf.register_opts(ALL_OPTS, group=GROUP_NAME)


def list_opts():
    return {GROUP_NAME: ALL_OPTS}