'''
This script is going to take in an orig_file and a prob_file. It will apply the prob_file on the orig_file to create the masked_file. It will also print the masked_file name to stdout.
'''
from aedev.nibble import load_probs, nib_mask
from sys import stderr
from sys import argv
import os

def main():
    if not len(argv)==3:
        print(f"applyMask.py called with incorrect arguments. argc: {len(argv)}", file=stderr)
        exit(2)
    orig_exe = argv[1]
    prob_file = argv[2]
    masked_file = nib_mask(orig_exe, load_probs(prob_file), "."+os.path.basename(prob_file)+".nibmask")
    print(masked_file)

    '''
    active_probs = "active_probs"
    orig_exes = "orig_exes"
    masked_dir = "masked_dir"
    if not os.path.isdir(active_probs):
        print(f"Active probabality files does not exist: {active_probs}\nPlease make it")
        return
    if not os.path.isdir(orig_exes):
        print(f"Original exes dirictory not found: {orig_exes}\nPlease make it")
        return
    
    # ps = load_probs(os.path.join(active_probs, "callOfTheWild.txt.pnp"))
    # masked_file = nib_mask("BouncyBall.exe", ps)

    print(f"Available probs: {os.listdir(active_probs)}")
    ap = len(os.listdir(active_probs))
    for i, d in enumerate(os.listdir(active_probs)):
        print(f"Applying probs ({i}/{ap}): {d}")
        ps = load_probs(os.path.join(active_probs, d))
        os.makedirs(masked_dir+"/"+d)
        od = len(os.listdir(orig_exes))
        for j, f in enumerate(os.listdir(orig_exes)):
            print(f"Masking file ({j}/{od}): {f}")
            masked_file = nib_mask(os.path.join(orig_exes, f), ps)
            os.rename(masked_file, os.path.join(masked_dir, d, os.path.basename(masked_file)))
            print("Masked file: " + os.path.basename(masked_file))
    '''
            


if __name__=='__main__':
    main()
    



