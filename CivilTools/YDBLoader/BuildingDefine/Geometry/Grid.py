from .Joint import Joint


class Grid:
    def __init__(self, id: int, s_joint: Joint, e_joint: Joint):
        if s_joint.std_flr_id != e_joint.std_flr_id:
            raise ValueError(
                "The standard-floor-ids of two Joints is not same! "
                + "Please check the data!"
            )
        self.id = id
        self.start_joint = s_joint
        self.end_joint = e_joint
        self.std_flr_id = s_joint.std_flr_id

    def get_length(self):
        return self.start_joint.distance_to_joint(self.end_joint)
