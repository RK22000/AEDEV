from aedev.nibble import prior_nib_prob, save_probs
from sys import stderr
import os

def main() -> None:
    ref_files = "ref_files"
    ref_probs = "ref_probs"
    if not os.path.isdir(ref_files):
        print(f"Reference file dirictory does not exist: {ref_files}", file=stderr)
        return
    if not os.path.isdir(ref_probs):
        os.makedirs(ref_probs)
    print (f"reading from ./{ref_files}/ -> writing to ./{ref_probs}/")
    for f in os.listdir(ref_files):
        ps = prior_nib_prob([f"{ref_files}/{f}"])
        save_probs(ps, f"{ref_probs}/{f}.pnp")
        print(f + " -> " + f + ".pnp")
        

if __name__ == "__main__":
    main()