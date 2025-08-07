use std::hash::poseidon2::Poseidon2::hash;

fn to_field_1d_64(input: [i64; 64]) -> [Field; 64] {
    let mut out: [Field; 64] = [0; 64];
    for i in 0..64 {
        out[i] = input[i] as Field;
    }
    out
}

fn to_field_1d_10(input: [i64; 10]) -> [Field; 10] {
    let mut out: [Field; 10] = [0; 10];
    for i in 0..10 {
        out[i] = input[i] as Field;
    }
    out
}

fn to_field_2d_64x784(input: [[i64; 784]; 64]) -> [[Field; 784]; 64] {
    let mut out: [[Field; 784]; 64] = [[0; 784]; 64];
    for i in 0..64 {
        for j in 0..784 {
            out[i][j] = input[i][j] as Field;
        }
    }
    out
}

fn to_field_2d_64x64(input: [[i64; 64]; 64]) -> [[Field; 64]; 64] {
    let mut out: [[Field; 64]; 64] = [[0; 64]; 64];
    for i in 0..64 {
        for j in 0..64 {
            out[i][j] = input[i][j] as Field;
        }
    }
    out
}

fn to_field_2d_10x64(input: [[i64; 64]; 10]) -> [[Field; 64]; 10] {
    let mut out: [[Field; 64]; 10] = [[0; 64]; 10];
    for i in 0..10 {
        for j in 0..64 {
            out[i][j] = input[i][j] as Field;
        }
    }
    out
}

fn hash_784(input: [Field; 784]) -> Field {
    hash(input, 784)
}

fn hash_64(input: [Field; 64]) -> Field {
    hash(input, 64)
}

fn hash_10(input: [Field; 10]) -> Field {
    hash(input, 10)
}

fn hash_6(input: [Field; 6]) -> Field {
    hash(input, 6)
}

fn hash_rows_64x784(input: [[Field; 784]; 64]) -> Field {
    let mut hashes: [Field; 64] = [0; 64];
    for i in 0..64 {
        hashes[i] = hash_784(input[i]);
    }
    hash_64(hashes)
}

fn hash_rows_64x64(input: [[Field; 64]; 64]) -> Field {
    let mut hashes: [Field; 64] = [0; 64];
    for i in 0..64 {
        hashes[i] = hash_64(input[i]);
    }
    hash_64(hashes)
}

fn hash_rows_10x64(input: [[Field; 64]; 10]) -> Field {
    let mut hashes: [Field; 10] = [0; 10];
    for i in 0..10 {
        hashes[i] = hash_64(input[i]);
    }
    hash_10(hashes)
}

pub fn generate_commitment(
    w1: [[i64; 784]; 64],
    b1: [i64; 64],
    w2: [[i64; 64]; 64],
    b2: [i64; 64],
    w3: [[i64; 64]; 10],
    b3: [i64; 10],
) -> Field {
    let fw1 = to_field_2d_64x784(w1);
    let fb1 = to_field_1d_64(b1);
    let fw2 = to_field_2d_64x64(w2);
    let fb2 = to_field_1d_64(b2);
    let fw3 = to_field_2d_10x64(w3);
    let fb3 = to_field_1d_10(b3);

    let h_w1 = hash_rows_64x784(fw1);
    let h_b1 = hash_64(fb1);
    let h_w2 = hash_rows_64x64(fw2);
    let h_b2 = hash_64(fb2);
    let h_w3 = hash_rows_10x64(fw3);
    let h_b3 = hash_10(fb3);

    let final_input = [h_w1, h_b1, h_w2, h_b2, h_w3, h_b3];
    hash_6(final_input)
}
