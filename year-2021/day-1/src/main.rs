use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut values = Vec::new();
    if let Ok(lines) = read_lines("./input.txt") {
        for line in lines {
            if let Ok(input) = line {
                // println!("Input: {}", input);
                values.push(input.parse::<i32>().unwrap());
            }
        }
    }
    answer(values);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn answer(values: Vec<i32>) {
    let mut increases = 0;
    let mut previous_value = values[0] + values[1] + values[2];
    let mut i = 1;
    
    while i < values.len() - 2 {
        let current_value = values[i] + values[i + 1] + values[i + 2];
        if current_value > previous_value {
            increases += 1;
        }
        previous_value = current_value;
        i += 1;
    }

    println!("Answer: {}", increases);
}
