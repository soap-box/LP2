import constants


def apply_permutation(inp, permutation_table, key_len):
    # helper function to apply permutation using provided P-Box
    result = 0
    permutation_len = len(permutation_table)
    for bit in range(permutation_len):
        result = result << 1  # make space for latest bit at lsb

        orig_bit_loc = permutation_table[bit]  # 1-indexed location of original bit
        current_bit = (inp >> (key_len - orig_bit_loc)) & 1  # get the bit at key[orig_bit_loc]
        result |= current_bit  # append current_bit to result

    return result


def cyclic_left_shift(val, pos, inp_bits):
    # helper function to cyclic left shift `val` by `pos` bits
    lost_bits = val >> (inp_bits - pos)
    val = val << pos
    val |= lost_bits

    val &= (1 << inp_bits) - 1  # keep result limited to max_bits bits
    return val


class DES:
    class DESKey:
        def __init__(self, key):
            if len(bin(key)) > 66:
                raise ValueError("Key Length should be less than or equal to 64 bits")

            self.key = key
            self.ip = apply_permutation(key, constants.PC1, 64)  # ip = initial permutation

        def get_round_keys(self):
            half_left = self.ip >> 28  # right shift ip by 28 bits
            half_right = self.ip & ((1 << 28)-1)  # mask higher 28 bits in ip

            keys = []
            num_rounds = 16
            for i in range(num_rounds):
                num_shifts = constants.KEYGEN_SHIFTS[i]
                half_left_shifted = cyclic_left_shift(half_left, num_shifts, 28)
                half_right_shifted = cyclic_left_shift(half_right, num_shifts, 28)

                half_left = half_left_shifted
                half_right = half_right_shifted

                round_key = (half_left_shifted << 28) | half_right_shifted
                round_key = apply_permutation(round_key, constants.PC2, 56)

                keys.append(round_key)

            return keys

    def __init__(self, key: int):
        self.key = self.DESKey(key)

    @staticmethod
    def round_func(round_inp, round_key):
        permuted_expanded_inp = apply_permutation(round_inp, constants.PE, 32)
        permuted_expanded_inp = permuted_expanded_inp ^ round_key
        substituted_round_op = 0
        for j in range(8):  # 8 groups of 6 bit each
            num_bits = 48 - 6 * (j+1)  # shift these number of bits right to get current 6 bits as lower 6 bits
            curr_bits = (permuted_expanded_inp >> num_bits)
            curr_bits &= (1 << 6) - 1  # only keep ls-6-bits

            sbox_row = (curr_bits & 1) | ((curr_bits >> 4) & 0b10)  # first and last bit
            sbox_col = (curr_bits >> 1) & 0xF  # middle 4 bits
            subs_val = constants.SBOX[j][sbox_row][sbox_col]

            substituted_round_op = substituted_round_op << 4  # make space for current value
            substituted_round_op |= subs_val

        permuted_value = apply_permutation(substituted_round_op, constants.PBOX, 32)

        return permuted_value

    def des_apply_rounds(self, msg, round_keys):
        if len(bin(msg)) > 66:
            raise ValueError("Length of input should be less than or equal to 64 bits")

        ip = apply_permutation(msg, constants.IP, 64)

        half_left_prev = ip >> 32  # right shift ip by 32 bits
        half_right_prev = ip & ((1 << 32) - 1)  # mask higher 32 bits in ip

        for i in range(16):
            current_key = round_keys[i]
            round_func_op = self.round_func(half_right_prev, current_key)

            left_curr = half_right_prev
            right_curr = half_left_prev ^ round_func_op

            # print(f"round {i+1}: {bin(left_curr << 32 | right_curr)}") # concatenate and display current round output

            half_left_prev, half_right_prev = left_curr, right_curr
            # break

        final_permutation_input = (half_right_prev << 32) | half_left_prev  # R16L16
        encrypted_msg = apply_permutation(final_permutation_input, constants.IP_INV, 64)

        return encrypted_msg

    def encrypt(self, message: int):
        round_keys = self.key.get_round_keys()
        return self.des_apply_rounds(message, round_keys)

    def decrypt(self, msg):
        round_keys = self.key.get_round_keys()[::-1]
        return self.des_apply_rounds(msg, round_keys)


def main():

    # generate key using
    # import secrets; key = secrets.randbits(64); print(f"key = {key} : {bin(key)[2:]} ({len(bin(key))-2} bits)")

    # https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm
    key = 0x133457799BBCDFF1  # 0b0001001100110100010101110111100110011011101111001101111111110001
    msg = 0x123456789abcdef  # 0b0000000100100011010001010110011110001001101010111100110111101111

    des = DES(key)
    enc = des.encrypt(msg)
    print(f"encrypted msg: {enc:X}")
    dec = des.decrypt(enc)
    print(f"decrypted msg: {dec:X}")


if __name__ == '__main__':
    main()
