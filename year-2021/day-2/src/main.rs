use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut values = Vec::new();
    if let Ok(lines) = read_lines("./input.txt") {
        for line in lines {
            if let Ok(input) = line {
                values.push(input);
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

fn answer(values: Vec<String>) {
    let mut horizontal = 0;
    let mut vertical = 0;
    let mut aim = 0;
    for value in values {
        // split the value into instructions
        let instruction: Vec<&str> = value.split(" ").collect();

        let instruction_value = instruction[1].parse::<i32>().unwrap();

        match instruction[0] {
            "forward" => {
                horizontal += instruction_value;
                vertical += aim * instruction_value;
            }
            "up" => aim -= instruction_value,
            "down" => aim += instruction_value,
            _ => println!("HERE"),
        }
    }
    println!("Answer: {}", horizontal * vertical);
}
