import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # If the page has no links, then have it link to all pages in the corpus   
    num_links = len(corpus[page])
    if num_links == 0:
        num_links = len(corpus)
   
    num_pages = len(corpus)
    proba_page = (1 - damping_factor) / num_pages # Probability of choosing a page at random
    keys = list(corpus.keys())
    distribution = dict.fromkeys(keys, proba_page) # Initialize distribution with equal probability for all pages
    proba_link = 1 / num_links # Probability of choosing a link at random from the current page
   
    # Iterate through all pages and check if a page is linked to by the current page
    for key in keys:
        if key in corpus[page]:
            distribution[key] += damping_factor * proba_link
    
    return distribution

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict.fromkeys(corpus.keys(), 0) # Initialize page ranks to 0
    
    # Initialize the distribution with equal probability for all pages
    for i in range(n):
        # Chooses a random page to start the sampling (if i == 0 then it simply chooses a random page, else it chooses a page based on the previous distribution)
        if i == 0:
            random_page = random.choice(list(corpus.keys()))
        else:
            random_page = random.choices(list(corpus.keys()), weights=list(distribution.values()), k=1)[0]
            
        page_ranks[random_page] += 1 # Increment the page rank for the chosen page
        distribution = transition_model(corpus, random_page, damping_factor) # Get the transition model for the chosen page for the next sample

    page_ranks = {page: rank / n for page, rank in page_ranks.items()} # Normalize the page ranks by dividing the number of occurences by the number of samples
    return page_ranks
    
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    proba = 1 / len(corpus)
    distribution = dict.fromkeys(corpus.keys(), proba) # Initialize distribution with equal probability for all pages
    proba_page = (1 - damping_factor) / len(corpus) # Probability of choosing a page at random
    
    # Iterate until convergence (i.e. the difference between the old and new distribution is less than 0.001)
    converged = False
    while not converged:
        old_distribution = distribution.copy()

        # Update the distribution for each page based on the links from other pages
        for page in sorted(corpus.keys()):
            page_ranks = 0
            
            # Goes through each link and checks if the page is linked to by that link
            for link in corpus.keys():
                links = list(corpus[link])
                
                # If the link has no links, then it links to all pages in the corpus
                if len(links) == 0:
                    links = list(corpus.keys())
                    corpus[link] = set(links)
                
                # If the page is linked to by the link, then add the probability of the link to the page ranks (sum of the probabilities of all links that link to the page)
                if page in corpus[link]:
                    page_ranks += (distribution[link] / len(links))
            
            distribution[page] = proba_page + (damping_factor * page_ranks) # Update the distribution for the page based on the sum of the probabilities of all links that link to the page       
        
        # Check for convergence by comparing the old and new distribution
        max_diff = 0
        for page in old_distribution:
            diff = abs(old_distribution[page] - distribution[page])
            if diff > max_diff:
                max_diff = diff 
        if max_diff < 0.001:
            converged = True

    return distribution
    raise NotImplementedError


if __name__ == "__main__":
    main()
