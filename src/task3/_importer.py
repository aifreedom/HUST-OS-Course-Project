if __name__ != "__main__":
    try: import gtkmvc
    except:
        import os.path; import sys
        top_dir = os.path.dirname(os.path.abspath(".."))
        sys.path = [top_dir] + sys.path
        import gtkmvc
        pass

    gtkmvc.require("1.0.0")
    
pass

