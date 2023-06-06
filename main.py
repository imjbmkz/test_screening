"""
Run as following:

python main.py "Customer name"
"""

# Import packages
import sys
import sanction_screening

if __name__=="__main__":

    argv = sys.argv

    if len(argv)==1:

        raise ValueError("Please enter the name to be screened.")
    
    else:

        name = argv[1]
        std_name = sanction_screening.transform_name(name)
        metaphone = sanction_screening.transform_name_metaphone(std_name)

        sanctions = sanction_screening.load_watchlist()
        sanctions["screeened_std"] = std_name
        sanctions["screeened_meta"] = metaphone
        sanctions["STD_NAME"] = sanctions["FULL_NAME"].map(sanction_screening.transform_name)
        sanctions["METAPHONE"] = sanctions["STD_NAME"].map(sanction_screening.transform_name_metaphone)
        sanctions["normal_ratio"] = sanctions["STD_NAME"].apply(sanction_screening.calc_ratio, args=(std_name, ))
        sanctions["metaphone_ratio"] = sanctions["METAPHONE"].apply(sanction_screening.calc_ratio, args=(metaphone, ))

        

        filter_res = (sanctions["normal_ratio"] >= 0.85) | (sanctions["metaphone_ratio"] >= 0.85)
        screening_results = sanctions[filter_res].copy()
        n_results = screening_results.shape[0]

        if n_results:
            screening_results.to_excel("results.xlsx", index=False)
            print("There are {} potential matches.".format(n_results))
            print(screening_results)