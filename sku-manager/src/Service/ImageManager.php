<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\Image;
use App\Entity\Product;
use App\Entity\System;
use App\Repository\ImageRepository;
use App\Service\Storage\StorageManagerInterface;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class ImageManager
{
    /**
     * @var ImageRepository
     */
    private ImageRepository $repository;

    private ValidatorInterface $validator;

    private StorageManagerInterface $storageManager;

    public function __construct(
        ImageRepository $repository,
        ValidatorInterface $validator,
        StorageManagerInterface $storageManager
    ) {
        $this->repository = $repository;
        $this->validator = $validator;
        $this->storageManager = $storageManager;
    }

    public function validate(Image $image)
    {
        return $this->validator->validate($image);
    }

    /**
     * @param Image $image
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateImage(Image $image): void
    {
        $this->repository->save($image);
    }

    /**
     * @param Image $image
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function persistImageFile(Image $image)
    {
        $this->updateImage($image);
        $image->setFileLocation(
            $image->getProduct()->getSystem()->getId()
            .'/'.$image->getProductId()
            .'/'.$image->getId().'_'.$image->getBaseFilename()
        );

        $data = base64_decode($image->getContent());

        $this->storageManager->uploadMediaFile($data, $image->getFileLocation());
        $publicUrl = $this->storageManager->getMediaPublicUrl($image->getFileLocation());
        $image->setSourceUrl($publicUrl);
    }

    public function getImage(int $id, System $system): ?Image
    {
        $image = $this->repository->findOneBy(['id' => $id, 'active' => true]);
        if ($image->getProduct() && $image->getProduct()->getSystem()->getId() === $system->getId()) {
            return $image;
        }

        return null;
    }

    /**
     * @param System $system
     *
     * @return Image[]
     */
    public function getImages(System $system)
    {
        return $this->repository->findAllBySystem($system);
    }

    public function getNewImage(Product $product): Image
    {
        $image = new Image();
        $image->setProduct($product);
        $image->setActive(true);
        $image->setCreatedDate(new DateTime());
        $image->setUpdatedDate(new DateTime());

        return $image;
    }

    public function deleteImage(Image $getImage)
    {
    }
}
