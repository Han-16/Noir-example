use std::hash::poseidon2::Poseidon2::hash;

fn main(age: Field, nonce: Field, min_age: pub Field, commitment: pub Field) {
    let hash_input = [age, nonce];
    let expected_commitment = hash(hash_input, 2);
    assert_eq(expected_commitment, commitment);
    assert(age as u32 >= min_age as u32);
}

#[test]
fn test_valid_age_and_commitment() {
    let age = 26;
    let nonce = 123;
    let min_age = 20;
    let commitment = hash([age, nonce], 2);
    main(age, nonce, min_age, commitment);
}

#[test(should_fail)]
fn test_invalid_age_too_young() {
    let age = 18;
    let nonce = 123;
    let min_age = 20;
    let commitment = hash([age, nonce], 2);
    main(age, nonce, min_age, commitment);
}

#[test(should_fail)]
fn test_invalid_commitment() {
    let age = 26;
    let nonce = 123;
    let min_age = 20;
    let commitment = hash([age, nonce + 1], 2);
    main(age, nonce, min_age, commitment);
}
