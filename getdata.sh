
DATA_DIR=".data"

SPAM_ASSN_URL="https://spamassassin.apache.org/publiccorpus"
SPAM_ASSN_EXT="tar.bz2"

for i in 20021010_easy_ham 20021010_hard_ham 20021010_spam 20030228_easy_ham 20030228_easy_ham_2 20030228_hard_ham 20030228_spam 20030228_spam_2 20050311_spam_2; do
  wget "$SPAM_ASSN_URL/$i.$SPAM_ASSN_EXT" -O "$DATA_DIR/$i.$SPAM_ASSN_EXT"
done

# Enron Data
ENRON_URL="http://www.aueb.gr/users/ion/data/enron-spam/raw"
ENRON_EXT="tar.gz"

# ham messages:
for i in beck-s farmer-d kaminski-v kitchen-l lokay-m williams-w3; do
  wget "$ENRON_URL/ham/$i.$ENRON_EXT" -O "$DATA_DIR/$i.$ENRON_EXT"
done

#spam messages:
for i in BG GP SH; do
  wget "$ENRON_URL/spam/$i.$ENRON_EXT" -O "$DATA_DIR/$i.$ENRON_EXT"
done

# Extract data
cd $DATA_DIR
for i in $(find . -type f -name '*.tar.*'); do
  tar zxvf $i
done
cd -
