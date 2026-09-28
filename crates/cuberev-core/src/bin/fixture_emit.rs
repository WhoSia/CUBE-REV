use cuberev_core::CornerState;
use std::env;

fn parse_vector(text: &str) -> Result<Vec<u8>, String> {
    text.split(',')
        .map(|part| {
            part.parse::<u8>()
                .map_err(|_| "MALFORMED_CANONICAL_PAYLOAD_REFUSE".to_string())
        })
        .collect()
}

fn fixed(values: Vec<u8>) -> Result<[u8; 7], String> {
    values
        .try_into()
        .map_err(|_| "MALFORMED_CANONICAL_PAYLOAD_REFUSE".to_string())
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 5 {
        eprintln!("MALFORMED_CANONICAL_PAYLOAD_REFUSE");
        std::process::exit(2);
    }
    let result = (|| -> Result<String, String> {
        let state = CornerState {
            perm: fixed(parse_vector(&args[1])?)?,
            ori: fixed(parse_vector(&args[2])?)?,
        };
        let rank = state
            .rank()
            .map_err(|_| "ILLEGAL_CUBIE_STATE_REFUSE".to_string())?;
        Ok(format!(
            "cs1|rank={rank}|frame={}|arm={}",
            state
                .symbolic_frame_bytes(&args[3])
                .map_err(|_| "ILLEGAL_CUBIE_STATE_REFUSE".to_string())?,
            args[4]
        ))
    })();
    match result {
        Ok(bytes) => println!("{bytes}"),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(3);
        }
    }
}
