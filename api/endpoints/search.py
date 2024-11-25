from typing import Union
from fastapi import APIRouter
from schemas.search import SearchResponse

router = APIRouter()

SEARCH_RESULTS = {
    "videos": [
        {
            "type": "video_result",
            "url": "https://www.youtube.com/watch?v=gpNshDIcvs8",
            "title": "Worst to Best FACE WASH for MEN *SHOCKING RESULTS* - YouTube",
            "description": "Top Face Wash Links are given below:1) *Muuchstac Ocean Face Wash :*Flipkart : https://bit.ly/K2243fkfwWebsite : https://bit.ly/K2243fwwebfwAmazon : https://",
            "age": "February 25, 2024",
            "page_age": "2024-02-25T06:30:22",
            "video": {},
            "meta_url": {
                "scheme": "https",
                "netloc": "youtube.com",
                "hostname": "www.youtube.com",
                "favicon": "https://imgs.search.brave.com/Wg4wjE5SHAargkzePU3eSLmWgVz84BEZk1SjSglJK_U/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvOTkyZTZiMWU3/YzU3Nzc5YjExYzUy/N2VhZTIxOWNlYjM5/ZGVjN2MyZDY4Nzdh/ZDYzMTYxNmI5N2Rk/Y2Q3N2FkNy93d3cu/eW91dHViZS5jb20v",
                "path": "› watch"
            },
            "thumbnail": {
                "src": "https://imgs.search.brave.com/ThSBAoH_4C7jL-egO6xu8vqPnJKjrDFUNfcPVLwNeQo/rs:fit:200:200:1:0/g:ce/aHR0cHM6Ly9pLnl0/aW1nLmNvbS92aS9n/cE5zaERJY3ZzOC9t/YXhyZXNkZWZhdWx0/LmpwZw",
                "original": "https://i.ytimg.com/vi/gpNshDIcvs8/maxresdefault.jpg",
                "logo": False  
            }
        },
        {
            "type": "video_result",
            "url": "https://www.youtube.com/watch?v=1BMctFtJQ5s",
            "title": "BEST FACEWASH FOR MEN IN WINTERS ❄️ | ASAD STYLING",
            "description": "Enjoy the videos and music you love, upload original content, and share it all with friends, family, and the world on YouTube.",
            "video": {},
            "meta_url": {
                "scheme": "https",
                "netloc": "youtube.com",
                "hostname": "www.youtube.com",
                "favicon": "https://imgs.search.brave.com/Wg4wjE5SHAargkzePU3eSLmWgVz84BEZk1SjSglJK_U/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvOTkyZTZiMWU3/YzU3Nzc5YjExYzUy/N2VhZTIxOWNlYjM5/ZGVjN2MyZDY4Nzdh/ZDYzMTYxNmI5N2Rk/Y2Q3N2FkNy93d3cu/eW91dHViZS5jb20v",
                "path": "› watch"
            },
            "thumbnail": {
                "src": "https://imgs.search.brave.com/MAGNVpafMeiaVMc21Y75ngEkkZb3-HnwwkIgPx2Hc9U/rs:fit:200:200:1:0/g:ce/aHR0cHM6Ly9pLnl0/aW1nLmNvbS92aS8x/Qk1jdEZ0SlE1cy9o/cWRlZmF1bHQuanBn",
                "original": "https://i.ytimg.com/vi/1BMctFtJQ5s/hqdefault.jpg"
            }
      }
        
    ],
    "web": [
        {
            "title": "Face Wash For Men | Best Face Wash & Cleanser for Oily Skin – The Man Company",
            "url": "https://www.themancompany.com/collections/face-washes",
            "is_source_local": False,
            "is_source_both": False,
            "description": "And once you decide to take on this journey from being a Man to modern Gentleman, The Man Company promises you to help you in the pursuit. ... Dive into our refreshing face washes and wash away impurities, excess oil and tan. ... An effective clarifying formula with a potent blend of Salicylic ...",
            "profile": {
                "name": "Themancompany",
                "url": "https://www.themancompany.com/collections/face-washes",
                "long_name": "themancompany.com",
                "img": "https://imgs.search.brave.com/pxkFXznxCsCTeootos220t_KVoTiO_XkwGOlu8pBqqk/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvOTEyMGQxM2I2/NDhlOWYzYjRhYTE0/MDJmNzA1YzE2Mjk1/NzRiMTMwM2U5ZTll/ZjI4NTY2NWE3YTYz/YjMyMmFjNy93d3cu/dGhlbWFuY29tcGFu/eS5jb20v"
            },
            "language": "en",
            "family_friendly": True,
            "type": "search_result",
            "subtype": "location",
            "is_live": False,
            "meta_url": {
                "scheme": "https",
                "netloc": "themancompany.com",
                "hostname": "www.themancompany.com",
                "favicon": "https://imgs.search.brave.com/pxkFXznxCsCTeootos220t_KVoTiO_XkwGOlu8pBqqk/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvOTEyMGQxM2I2/NDhlOWYzYjRhYTE0/MDJmNzA1YzE2Mjk1/NzRiMTMwM2U5ZTll/ZjI4NTY2NWE3YTYz/YjMyMmFjNy93d3cu/dGhlbWFuY29tcGFu/eS5jb20v",
                "path": "  › translation missing: en.general.breadcrumb.home  › face washes for men"
            },
            "thumbnail": {
                "src": "https://imgs.search.brave.com/7Rex-Lr6rxqCmoOLnm4PkBNsBP1UmFVjfvlxwBrzqjY/rs:fit:200:200:1:0/g:ce/aHR0cHM6Ly93d3cu/dGhlbWFuY29tcGFu/eS5jb20vY2RuL3No/b3BpZnljbG91ZC9z/aG9waWZ5L2Fzc2V0/cy9uby1pbWFnZS0y/MDQ4LTVlODhjMWIy/MGUwODdmYjdiYmU5/YTM3NzE4MjRlNzQz/YzI0NGY0MzdlNGY4/YmE5M2JiZjdiMTFi/NTNmNzgyNGNfZ3Jh/bmRlLmdpZg.jpeg",
                "original": "https://www.themancompany.com/cdn/shopifycloud/shopify/assets/no-image-2048-5e88c1b20e087fb7bbe9a3771824e743c244f437e4f8ba93bbf7b11b53f7824c_grande.gif",
                "logo": False
            }
        },
           {
        "title": "Men's Face Wash | Buy Face Wash for Men Online in India at Best Price",
        "url": "https://www.myntra.com/men-face-wash",
        "is_source_local": False,
        "is_source_both": False,
        "description": "Buy wide range of <strong>face</strong> <strong>wash</strong> <strong>for</strong> <strong>men</strong> online in India. Choose from refreshing &amp; clarifying <strong>face</strong> <strong>wash</strong> by top brands, to get clean skin every day. ✯Free Shipping ✯Cash on Delivery ✯30-day returns",
        "profile": {
          "name": "Myntra",
          "url": "https://www.myntra.com/men-face-wash",
          "long_name": "myntra.com",
          "img": "https://imgs.search.brave.com/m-o7f7eRfvaKKjuyJQGX9nkaZvMXrFWENTlfR4GmIIY/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMTUzZmRhYmEz/NjY2MmNiNWUzZWFl/Zjg4MDVmOTA2MTMy/MGI4Y2RkNDJhMGM4/NTI2ZmEyMzQ0NDE5/MDllODRkMC93d3cu/bXludHJhLmNvbS8"
        },
        "language": "en",
        "family_friendly": True,
        "type": "search_result",
        "subtype": "generic",
        "is_live": False,
        "meta_url": {
          "scheme": "https",
          "netloc": "myntra.com",
          "hostname": "www.myntra.com",
          "favicon": "https://imgs.search.brave.com/m-o7f7eRfvaKKjuyJQGX9nkaZvMXrFWENTlfR4GmIIY/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMTUzZmRhYmEz/NjY2MmNiNWUzZWFl/Zjg4MDVmOTA2MTMy/MGI4Y2RkNDJhMGM4/NTI2ZmEyMzQ0NDE5/MDllODRkMC93d3cu/bXludHJhLmNvbS8",
          "path": "  › home  › personal care  › mens face wash"
        },
        "thumbnail": {
          "src": "https://imgs.search.brave.com/NfAv13AGtSRgVQg97JzKDEPwDDGdzbCBH3gFTB16RlM/rs:fit:200:200:1:0/g:ce/aHR0cHM6Ly9jb25z/dGFudC5teW50YXNz/ZXRzLmNvbS93d3cv/ZGF0YS9wb3J0YWwv/bWxvZ28ucG5n",
          "original": "https://constant.myntassets.com/www/data/portal/mlogo.png",
          "logo": True
        }
      },
    {
        "title": "Men Face Wash - Buy Men Face Wash Online at Best Prices In India | Flipkart.com",
        "url": "https://www.flipkart.com/beauty-and-grooming/body-face-skin-care/body-and-face-care/face-wash/men~idealfor/pr?sid=g9b,ema,5la,jav&page=6",
        "is_source_local": False,
        "is_source_both": False,
        "description": "<strong>Glamveda Face Wash ,Terrai Face</strong> ... Face Wash ... SponsoredGarnier Men Turbo Bright Double Action,150gm (Pack of 2... ... VLCC Ayurveda Skin Brightening Haldi &amp; Chandan Deep Cl... ... L&#x27;Oréal Paris Revitalift Hyaluronic Acid Hydrating Gel ... ... SponsoredWOW SKIN SCIENCE Ubtan For Oily Skin- ...",
        "profile": {
          "name": "Flipkart",
          "url": "https://www.flipkart.com/beauty-and-grooming/body-face-skin-care/body-and-face-care/face-wash/men~idealfor/pr?sid=g9b,ema,5la,jav&page=6",
          "long_name": "flipkart.com",
          "img": "https://imgs.search.brave.com/DoMJ3DLNQoT2zzLDzL-NlfEmHIHDx64eJf2C7svoZOA/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvY2QwNjRmNWVh/MTcyMDIzNjk0OGQ1/M2IxMTI4ZWI3NWJh/NWZiMDk0NWYwYTgz/MzcxYzQyYjJjYTk3/MDFiNDVmMy93d3cu/ZmxpcGthcnQuY29t/Lw"
        },
        "language": "en",
        "family_friendly": True,
        "type": "search_result",
        "subtype": "generic",
        "is_live": False,
        "meta_url": {
          "scheme": "https",
          "netloc": "flipkart.com",
          "hostname": "www.flipkart.com",
          "favicon": "https://imgs.search.brave.com/DoMJ3DLNQoT2zzLDzL-NlfEmHIHDx64eJf2C7svoZOA/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvY2QwNjRmNWVh/MTcyMDIzNjk0OGQ1/M2IxMTI4ZWI3NWJh/NWZiMDk0NWYwYTgz/MzcxYzQyYjJjYTk3/MDFiNDVmMy93d3cu/ZmxpcGthcnQuY29t/Lw",
          "path": "› beauty-and-grooming  › body-face-skin-care  › body-and-face-care  › face-wash  › men~idealfor  › pr"
        }
      },
          {
        "title": "Amazon.in: Facewash For Men",
        "url": "https://www.amazon.in/facewash-for-men/s?k=facewash+for+men",
        "is_source_local": False,
        "is_source_both": False,
        "description": "Muuchstac Ocean <strong>Face</strong> <strong>Wash</strong> <strong>for</strong> <strong>Men</strong> | Fight Acne &amp; Pimples, Brighten Skin, Clears Dirt, Oil Control, Refreshing Feel - Multi-Action Formula (2x100 ml) · After viewing product detail pages, look here to find an easy way to navigate back to pages you are interested in",
        "profile": {
          "name": "Amazon",
          "url": "https://www.amazon.in/facewash-for-men/s?k=facewash+for+men",
          "long_name": "amazon.in",
          "img": "https://imgs.search.brave.com/VaPpXqEJLdIWx7txvtpuqIlJica0TTEjPb8Aj1ACQDc/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMjk5MTcxYzBl/M2E4ZTFkZTVlMDBi/ODJjOGZiNzNjZjRm/ZDkxMzMxN2M3ZTA4/MGRiZmYzNGU2YTk0/YmFlZTI5Zi93d3cu/YW1hem9uLmluLw"
        },
        "language": "en",
        "family_friendly": True,
        "type": "search_result",
        "subtype": "generic",
        "is_live": False,
        "meta_url": {
          "scheme": "https",
          "netloc": "amazon.in",
          "hostname": "www.amazon.in",
          "favicon": "https://imgs.search.brave.com/VaPpXqEJLdIWx7txvtpuqIlJica0TTEjPb8Aj1ACQDc/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMjk5MTcxYzBl/M2E4ZTFkZTVlMDBi/ODJjOGZiNzNjZjRm/ZDkxMzMxN2M3ZTA4/MGRiZmYzNGU2YTk0/YmFlZTI5Zi93d3cu/YW1hem9uLmluLw",
          "path": "› facewash-for-men  › s"
        }
      },
      {
        "title": "Face Wash for Men and Women at Best Price in India",
        "url": "https://mamaearth.in/product-category/face-wash",
        "is_source_local": False,
        "is_source_both": False,
        "description": "Best <strong>face</strong> <strong>wash</strong> range online in India. Mamaearth&#x27;s natural &amp; chemical-free best <strong>face</strong> <strong>wash</strong> <strong>for</strong> <strong>men</strong> and women makes the basics of a perfect AM-PM routine",
        "profile": {
          "name": "Mamaearth",
          "url": "https://mamaearth.in/product-category/face-wash",
          "long_name": "mamaearth.in",
          "img": "https://imgs.search.brave.com/u_uFHc_mJWC038Ov8tQ0JbrqTETESZE2Lx-86sSFaI4/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvNDA2ZGZhMTIx/ZTQzNDk5N2E2MzU4/M2JiMDc4MmVlMjU4/MTk2MmI5OTUwMGE4/MWM3YzA5YTRiMzY1/MzE2NDE0MC9tYW1h/ZWFydGguaW4v"
        },
        "language": "en",
        "family_friendly": True,
        "type": "search_result",
        "subtype": "faq",
        "is_live": False,
        "meta_url": {
          "scheme": "https",
          "netloc": "mamaearth.in",
          "hostname": "mamaearth.in",
          "favicon": "https://imgs.search.brave.com/u_uFHc_mJWC038Ov8tQ0JbrqTETESZE2Lx-86sSFaI4/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvNDA2ZGZhMTIx/ZTQzNDk5N2E2MzU4/M2JiMDc4MmVlMjU4/MTk2MmI5OTUwMGE4/MWM3YzA5YTRiMzY1/MzE2NDE0MC9tYW1h/ZWFydGguaW4v",
          "path": "  › home  › face wash"
        },
        "thumbnail": {
          "src": "https://imgs.search.brave.com/OMM5Uup1FQzBD3cO0yasklexA75v-244RFKgWXSndXM/rs:fit:200:200:1:0/g:ce/aHR0cHM6Ly9zdC1p/bWFnZXMuaG9uYXNh/LmluL01vYmlsZV9G/V19jb3B5X2U0OTA4/MmU2YjMuZ2lm.jpeg",
          "original": "https://st-images.honasa.in/Mobile_FW_copy_e49082e6b3.gif",
          "logo": False
        }
      }       
    ]
}

@router.get("/search", response_model=SearchResponse)
async def search():
    return SEARCH_RESULTS