# Feedback class
class Feedback:
    count_id = 0

    # initializer method
    def __init__(self,membership, remarks):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id

        self.__membership = membership
        self.__remarks = remarks

    # accessor methods
    def get_feedback_id(self):
        return self.__feedback_id


    def get_membership(self):
        return self.__membership

    def get_remarks(self):
        return self.__remarks

    # mutator methods
    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id


    def set_membership(self, membership):
        self.__membership = membership

    def set_remarks(self, remarks):
        self.__remarks = remarks