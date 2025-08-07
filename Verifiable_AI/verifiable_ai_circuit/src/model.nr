pub fn inference(
    x: [i64; 784],
    w1: [[i64; 784]; 64],
    b1: [i64; 64],
    w2: [[i64; 64]; 64],
    b2: [i64; 64],
    w3: [[i64; 64]; 10],
    b3: [i64; 10],
    scale: i64,
) -> i64 {
    let h1 = linear_relu_64_784(x, w1, b1, scale);
    let h2 = linear_relu_64_64(h1, w2, b2, scale);
    let out = linear_10(h2, w3, b3, scale);
    let pred = argmax(out);
    pred
}


fn linear_relu_64_784(
    x: [i64; 784],
    w: [[i64; 784]; 64],
    b: [i64; 64],
    scale: i64,
) -> [i64; 64] {
    let mut out: [i64; 64] = [0; 64];

    for i in 0..64 {
        let mut acc = 0;
        for j in 0..784 {
            acc = dot_mul_add(acc, x[j], w[i][j]);
        }
        acc = apply_scale_and_bias(acc, scale, b[i]);
        out[i] = relu(acc);
    }

    out
}

fn linear_relu_64_64(x: [i64; 64], w: [[i64; 64]; 64], b: [i64; 64], scale: i64) -> [i64; 64] {
    let mut out: [i64; 64] = [0; 64];

    for i in 0..64 {
        let mut acc = 0;
        for j in 0..64 {
            acc = dot_mul_add(acc, x[j], w[i][j]);
        }
        acc = apply_scale_and_bias(acc, scale, b[i]);
        out[i] = relu(acc);
    }

    out
}

fn linear_10(x: [i64; 64], w: [[i64; 64]; 10], b: [i64; 10], scale: i64) -> [i64; 10] {
    let mut out: [i64; 10] = [0; 10];

    for i in 0..10 {
        let mut acc = 0;
        for j in 0..64 {
            acc = dot_mul_add(acc, x[j], w[i][j]);
        }
        out[i] = apply_scale_and_bias(acc, scale, b[i]);
    }

    out
}

fn argmax(logits: [i64; 10]) -> i64 {
    let mut max_val = logits[0];
    let mut max_idx = 0;

    for i in 1..10 {
        if logits[i] > max_val {
            max_val = logits[i];
            max_idx = i;
        }
    }

    max_idx as i64
}

fn relu(x: i64) -> i64 {
   if x > 0 { x } else { 0 }
}

fn dot_mul_add(acc: i64, x: i64, w: i64) -> i64 {
    acc + x * w
}

fn apply_scale_and_bias(acc: i64, scale: i64, bias: i64) -> i64 {
    acc / scale + bias
}