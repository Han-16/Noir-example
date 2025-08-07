mod utils;
mod model;
use model::inference;
use utils::generate_commitment;

fn main(
    x: pub [i64; 784],
    w1: [[i64; 784]; 64],
    b1: [i64; 64],
    w2: [[i64; 64]; 64],
    b2: [i64; 64],
    w3: [[i64; 64]; 10],
    b3: [i64; 10],
    scale: i64,
    y: pub i64,
    commitment: pub Field,
) {
    let pred = inference(x, w1, b1, w2, b2, w3, b3, scale);
    assert(pred == y);

    let expected_commitment = generate_commitment(w1, b1, w2, b2, w3, b3);
    // println(expected_commitment);
    assert(commitment == expected_commitment);
}
