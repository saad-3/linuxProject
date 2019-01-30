from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Brand, Base, Product, User

engine = create_engine('postgresql:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



user1 = User(name = "saad alqahtani", email="saad@udacity.com")
session.add(user1)
session.commit()


brand1 = Brand(name="Apple", user_id=1 )
session.add(brand1)
session.commit()

brand2 = Brand(name="Samsung", user_id=1)
session.add(brand2)
session.commit()

brand3 = Brand(name="Huawei", user_id=1)
session.add(brand3)
session.commit()

product1 = Product(name="iphone Xs", description="""The iPhone XS
    display has rounded corners that follow a beautiful curved design,
    and these corners are within a standard rectangle. When measured
    as a standard rectangular shape, the screen is 5.85 inches
    diagonally (actual viewable area is less).""", price="999$",
    brand_id=1, user_id=1)
session.add(product1)
session.commit()

product2 = Product(name="iPad Pro", description="""The iPad Pro
    is a 12.9-inch tablet with 2,732 x 2,048 pixel resolution that
    is nearly as thin (6.9mm) as the company's iPad Air while weighing
    about the same (1.59 pounds) as Apple's original
    iPad device.""", price="799$", brand_id=1, user_id=1)
session.add(product2)
session.commit()

product3 = Product(name="MacBook Pro", description="""The MacBook Pro is a
    brand of Macintosh laptop computers by Apple Inc. that merged the
    PowerBook and iBook lines during Apple's transition to Intel
    processors. The current lineup consists of the MacBook (2015-present),
     the MacBook Air (2008-present), and the MacBook Pro
     (2006-present).""", price="1849$", brand_id=1, user_id=1)
session.add(product3)
session.commit()

product4 = Product(name="Galaxy S9", description=""" Samsung Galaxy S9 is
    expected to boast of a 12-megapixel primary camera on the rear and
    an 8-megapixel front shooter for selfies. This smartphone is rumored
    to have 64GB of internal storage that can be expanded up to 256GB via
    a microSD card.""", price="719$", brand_id=2, user_id=1)
session.add(product4)
session.commit()

product5 = Product(name="Galaxy Tab S4", description=""" The tablet comes
    with a 10.50-inch touchscreen display with a resolution of 2560 pixels
     by 1600 pixels at a PPI of 287 pixels per inch. The Samsung Galaxy
      Tab S4 (Wi-Fi) is powered by 2.35GHz octa-core processor and it
      comes with 4GB of RAM.""", price="729$", brand_id=2, user_id=1)
session.add(product5)
session.commit()

product6 = Product(name="Galaxy Note9", description=""" The Note 9 has
    a 6.4 inches (160 mm) 1440p Super AMOLED display with an 18.5:9 aspect
     ratio. The design on the front is otherwise similar to the Note 8,
      using an "Infinity Display" as marketed by
      Samsung.""", price="999$", brand_id=2, user_id=1)
session.add(product6)
session.commit()

product7 = Product(name="Mate 20 Pro", description=""" The Mate 20 Pro
    is a slightly smaller phone, but rocks an impressive 6.39-inch curved
     OLED display, running a 3,120 x 1,440 resolution in a 19.5:9 aspect
     ratio.You'll find a fingerprint sensor on the back of the Mate 20 - but
     it's missing on the
      Mate 20 Pro.""", price="829$", brand_id=3, user_id=1)
session.add(product7)
session.commit()

product8 = Product(name="Nova 3", description=""" The Huawei Nova 3
    mobile features a 6.3" (16 cm) display with a screen resolution of
    1080 x 2340 pixels and runs on Android v8.1 (Oreo) operating system.
     The device is powered by Octa core (2.36 GHz, Quad core,
     Cortex A73 + 1.8 GHz, Quad core, Cortex A53) processor paired with
      6 GB of RAM.""", price="289$", brand_id=3, user_id=1)
session.add(product8)
session.commit()

product9 = Product(name="MateBook X Pro", description=""" the MateBook X
    Pro measures only 0.57-inch thin and weighs less than 3 pounds.
     For the first time, FullView is defined for a laptop giving you
     an immersive experience with 3K FullView touchscreen at 91%
     screen-to-body ratio.""", price="1199$", brand_id=3, user_id=1)
session.add(product9)
session.commit()


print "demo successfully added! "
