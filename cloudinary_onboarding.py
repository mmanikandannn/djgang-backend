
import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary.utils import cloudinary_url


cloudinary.config(
    cloud_name="bukhle9v",
    api_key="381616936966587",
    api_secret="MiI2c29t24Qjl-PnuK0aa2YYDLA",
    secure=True,
)


def main():
    sample_image_url = (
        "https://res.cloudinary.com/demo/image/upload/sample.jpg"
    )

    upload_result = cloudinary.uploader.upload(
        sample_image_url,
        folder="djchemboi_onboarding",
        overwrite=True,
    )

    secure_url = upload_result["secure_url"]
    public_id = upload_result["public_id"]

    print("Uploaded image URL:", secure_url)
    print("Public ID:", public_id)

    details = cloudinary.api.resource(public_id)

    print("Width:", details["width"])
    print("Height:", details["height"])
    print("Format:", details["format"])
    print("File size in bytes:", details["bytes"])

    # f_auto selects the most efficient supported image format.
    # q_auto automatically balances image quality and file size.
    transformed_url, _ = cloudinary_url(
        public_id,
        fetch_format="auto",
        quality="auto",
        secure=True,
    )

    print(
        "Done! Click the link below to see the optimized version "
        "of the image. Check the size and format."
    )
    print("Transformed image URL:", transformed_url)


if __name__ == "__main__":
    main()


