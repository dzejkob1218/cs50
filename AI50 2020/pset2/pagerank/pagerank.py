import os
import random
import re
import sys
import bisect

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
    # the probability that any page will be chosen at random as result of damping
    init_prob = 1 - damping_factor if corpus[page] else 1
    # initialize dictionary with same keys as corpus and distribute initial probability
    probs = dict.fromkeys(corpus.keys(), init_prob / len(corpus))
    # the added probability of a link being followed
    for link in corpus[page]:
        probs[link] += damping_factor / len(corpus[page])
    return probs


def bisection_points(weights):
    result = []
    sum = 0
    for weight in weights:
        sum += weight
        result.append(sum)
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    results = dict.fromkeys(corpus.keys(), 0)

    # make a list with all pages in the corpus
    pages = list(corpus.keys())

    # create a list with accumulated probabilities corresponding to the order of pages in the list created above
    cumulative_trans_models = {}
    for page in corpus:
        new_model = []
        model_dict = transition_model(corpus, page, DAMPING)
        cumu_sum = 0
        for p in pages:
            cumu_sum += model_dict[p]
            new_model.append(cumu_sum)
        cumulative_trans_models[page] = new_model

    # start with a random sample
    sample = random.choice(pages)
    # sample n times
    for i in range(n):
        results[sample] += 1  # count prev sample
        probs = cumulative_trans_models[sample]
        choice = bisect.bisect(probs, random.random())  # get the page at random threshold
        sample = pages[choice]

    for r in results:
        results[r] /= n
    return results


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize ranks with all pages of equal probability
    ranks = dict.fromkeys(corpus.keys(), 1 / len(corpus))
    # for each page get a set of other pages that link to it
    incoming_links = {new_set: set() for new_set in corpus.keys()}
    for page in corpus:
        if corpus[page]:
            for link in corpus[page]:
                incoming_links[link].add(page)
        else:  # if a page has no links, treat it as if it has a link for every page
            for p in incoming_links:
                incoming_links[p].add(page)

    # calculate new rank values until they converge
    convergence = False
    while not convergence:
        convergence = True
        for r in ranks:
            links_sum = 0
            for i in incoming_links[r]:
                links_sum += ranks[i] / (len(corpus[i]) if len(corpus[i]) else len(corpus))
            old_value = ranks[r]
            ranks[r] = (1 - damping_factor) / len(corpus) + damping_factor * links_sum
            difference = abs(old_value - ranks[r])
            if difference > 0.001:
                convergence = False
    return ranks


if __name__ == "__main__":
    main()
