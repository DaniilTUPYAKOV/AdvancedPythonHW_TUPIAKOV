import aiofiles
import aiohttp
import asyncio
import os


async def save_image(path: str, image: memoryview) -> None:
    """Save image with aiofiles"""
    async with aiofiles.open(path, "wb") as file:
        await file.write(image)


async def download_image(session, url, folder, file_name) -> None:
    """ " Task body, aiohttp download picture and await of saving it"""

    async with session.get(url) as response:

        picture = await response.read()

        await save_image(os.path.join(folder, file_name), picture)

        print(f"Picture {file_name} succesfully downloaded")


async def main(url, folder, number_of_images):
    """Main body, creates mupltiple tasks and awaits them"""

    if not os.path.exists(folder):
        os.makedirs(folder)

    async with aiohttp.ClientSession() as session:

        await asyncio.gather(
            *[
                download_image(session, url, folder, f"image_{i}.jpg")
                for i in range(number_of_images)
            ]
        )


URL = "https://source.unsplash.com/random"
RELATIVE_PATH_TO_FOLDER = "hw_5/artifacts"
NUMBER_OF_IMAGES = 10

if __name__ == "__main__":
    asyncio.run(main(URL, RELATIVE_PATH_TO_FOLDER, NUMBER_OF_IMAGES))
