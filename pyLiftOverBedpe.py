import argparse
from pyliftover import LiftOver

def lift_bedpe(input_bedpe, output_bedpe, chainfile):
    converter = LiftOver(chainfile)

    with open(input_bedpe, 'r') as infile, open(output_bedpe, 'w') as outfile:
        for line in infile:
            fields = line.strip().split()
            chrom1, start1, end1 = fields[0], int(fields[1]), int(fields[2])
            chrom2, start2, end2 = fields[3], int(fields[4]), int(fields[5])
            extra_fields = fields[6:]  # Preserve additional columns

            # Lift over the first region
            lifted_start1 = converter.convert_coordinate(chrom1, start1)
            lifted_end1 = converter.convert_coordinate(chrom1, end1)

            # Lift over the second region
            lifted_start2 = converter.convert_coordinate(chrom2, start2)
            lifted_end2 = converter.convert_coordinate(chrom2, end2)

            # Check if both regions were successfully lifted over
            if lifted_start1 and lifted_end1 and lifted_start2 and lifted_end2:
                # Extract lifted coordinates
                lifted_chrom1, lifted_start1_pos = lifted_start1[0][0], lifted_start1[0][1]
                lifted_chrom2, lifted_start2_pos = lifted_start2[0][0], lifted_start2[0][1]
                lifted_end1_pos = lifted_end1[0][1]
                lifted_end2_pos = lifted_end2[0][1]

                # Ensure start <= end for both regions
                if lifted_start1_pos > lifted_end1_pos:
                    lifted_start1_pos, lifted_end1_pos = lifted_end1_pos, lifted_start1_pos
                if lifted_start2_pos > lifted_end2_pos:
                    lifted_start2_pos, lifted_end2_pos = lifted_end2_pos, lifted_start2_pos

                # Write the lifted BEDPE line with extra fields
                outfile.write(
                    f"{lifted_chrom1}\t{lifted_start1_pos}\t{lifted_end1_pos}\t"
                    f"{lifted_chrom2}\t{lifted_start2_pos}\t{lifted_end2_pos}\t"
                    + '\t'.join(extra_fields) + "\n"
                )
            else:
                print(f"Skipping unmapped region: {line.strip()}")

def main():
    parser = argparse.ArgumentParser(
        description="Lift over a BEDPE file from one genome assembly to another.",
        epilog="Usage: python pyLiftOverBedpe.py -i input.bedpe -o output.bedpe -c hg19ToHg38.over.chain"
    )
    parser.add_argument("-i", "--input", required=True, help="Input BEDPE file")
    parser.add_argument("-o", "--output", required=True, help="Output BEDPE file with lifted coordinates")
    parser.add_argument("-c", "--chainfile", required=True, help="Path to the chain file for liftover")
    args = parser.parse_args()

    lift_bedpe(args.input, args.output, args.chainfile)

if __name__ == "__main__":
    main()
