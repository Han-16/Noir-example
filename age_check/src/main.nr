use std::hash::poseidon2::Poseidon2::hash;

fn main(age: Field, nonce: Field, min_age: pub Field, commitment: pub Field) {
    let hash_input = [age, nonce];
    let expected_commitment = hash(hash_input, 2);
    assert_eq(expected_commitment, commitment);
    assert(age as u32 >= min_age as u32);
}

#[test]
fn test_main() {
    let age = 26;
    let nonce = 123;
    let min_age = 20;
    let commitment = hash([age, nonce], 2); // 0x2f683e77989e13752c0ebd3f86a1bb6422424e05007c3d34336c765b432251f0
    main(age, nonce, min_age, commitment);
}
