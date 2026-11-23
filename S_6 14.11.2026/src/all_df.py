def load_all(raw_dir):
    trips=load_trips(raw_dir)
    carriers=load_carriers(raw_dir)
    return {'trips':trips,'carriers':carriers}