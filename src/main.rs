use std::fs;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::env;
use std::process::Command;

static SEED:u64 = 0x1337;

fn rand() -> u64{
    let mut rand_num:u64 = 0;
    rand_num ^= (SEED << 13) & 0xffffffffffffffff;
    rand_num ^= (rand_num << 17) & 0xffffffffffffffff;
    rand_num ^= (rand_num << 43) & 0xffffffffffffffff;

    return rand_num
}

fn main() {
    println!("IDK fuzzer v0.1.0 objdump");
    
    let args: Vec<String> = env::args().collect();
    
    let option= &args[1];   // Option1 : STDIN ? Option2 : FileIO ?

    fs::create_dir_all("corpus").expect("Failed to create path");
    let rand_num = rand();
    
    let path_name: String = "corpus/".to_string() + &rand_num.to_string();
    let path = Path::new(&path_name);
    let mut file = match File::create(&path) {
        Err(why) => panic!("couldn't create directory {}",why),
        Ok(file) => file,
    };
    file.write_all(&rand_num.to_be_bytes());
    
    Command::new("objdump")
        .arg("-s")
        .arg(path_name)
        .spawn()
        .expect("Failed to launch objdump");
}
