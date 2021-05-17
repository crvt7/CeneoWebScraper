class opinion:
    def __init__(self, author, recommendation, stars, confirmed, date, dateOfPurchase, useful, useless, text, pros, cons):
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.confirmed = confirmed
        self.date = date
        self.dateOfPurchase = dateOfPurchase
        self.useful = useful
        self.useless = useless
        self.text = text
        self.pros = pros
        self.cons = cons
    
    def __repr__(self):
        print(f""" 
        Author: {self.author}
        Recommendation: {self.recommendation}
        Number of stars: {self.stars}
        Confirmed by purchase: {self.confirmed}
        Date of submission: {self.date}
        Date of purchase: {self.dateOfPurchase}
        Number of people who thought the review was useful: {self.useful}
        Number of people who thought the review was useless: {self.useless}
        Content of the review: {self.text}
        Pros: {self.pros}
        Cons: {self.cons}
        """)
