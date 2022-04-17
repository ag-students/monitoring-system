from app.models import sampleData

def create_sample_list():
    data1_0 = sampleData(
        id_room     = 1,
        day_part    = 0,
        time_diff   = 60,
        timer       = 60
    )
    data1_1 = sampleData(
        id_room     = 1,
        day_part    = 1,
        time_diff   = 60,
        timer       = 60
    )
    data1_2 = sampleData(
        id_room     = 1,
        day_part    = 2,
        time_diff   = 60,
        timer       = 60
    )
    data1_3 = sampleData(
        id_room     = 1,
        day_part    = 3,
        time_diff   = 60,
        timer       = 60
    )
    data2_0 = sampleData(
        id_room     = 2,
        day_part    = 0,
        time_diff   = 60,
        timer       = 60
    )
    data2_1 = sampleData(
        id_room     = 2,
        day_part    = 1,
        time_diff   = 60,
        timer       = 60
    )
    data2_2 = sampleData(
        id_room     = 2,
        day_part    = 2,
        time_diff   = 60,
        timer       = 60
    )
    data2_3 = sampleData(
        id_room     = 2,
        day_part    = 3,
        time_diff   = 60,
        timer       = 60
    )

    sample_list = [data1_0, data1_1, data1_2, data1_3,
                   data2_0, data2_1, data2_2, data2_3]
    return sample_list

def edit_sample():
    # find by mac address and part day
    # then update row
    return