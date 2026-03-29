<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Entity\Product;
use App\Event\ImageManagement\AddImageEvent;
use App\Event\ImageManagement\AddImageValidEvent;
use App\Event\ImageManagement\DeleteImageEvent;
use App\Event\ImageManagement\DeleteImageValidEvent;
use App\Event\ImageManagement\UpdateImageEvent;
use App\Event\ImageManagement\UpdateImageValidEvent;
use App\Form\ImageType;
use App\Service\ImageManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;

class ImageManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private ImageManager $imageManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        ImageManager $imageManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->imageManager = $imageManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddImageEvent::class => 'onAddImage',
            AddImageValidEvent::class => 'onAddImageValid',
            UpdateImageEvent::class => 'onUpdateImage',
            UpdateImageValidEvent::class => 'onUpdateImageValid',
            DeleteImageEvent::class => 'onDeleteImage',
            DeleteImageValidEvent::class => 'onDeleteImageValid',
        ];
    }

    public function onAddImage(AddImageEvent $event)
    {
        $image = $this->imageManager->getNewImage(new Product());

        $event->setImage($image);

        $form = $this->formFactory->create(ImageType::class, $image);
        $data = json_decode($event->getRequest()->getContent(), true);
        $form->submit($data);

        if (!$form->isValid()) {
            $response = new ResponseDataDto(
                $form->getErrors(true),
                Response::HTTP_BAD_REQUEST
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param AddImageValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onAddImageValid(AddImageValidEvent $event)
    {
        $this->imageManager->persistImageFile($event->getImage());
        $this->imageManager->updateImage($event->getImage());
    }

    public function onDeleteImage(DeleteImageEvent $event)
    {
        $image = $this->imageManager->getImage($event->getId(), $event->getSystem());
        if (!$image) {
            $response = new ResponseDataDto(
                ['message' => 'Image not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    public function onDeleteImageValid(DeleteImageValidEvent $event)
    {
        $this->imageManager->deleteImage($event->getImage());
    }

    public function onUpdateImage(UpdateImageEvent $event)
    {
        $image = $this->imageManager->getImage($event->getId(), $event->getSystem());
        if (!$image) {
            $response = new ResponseDataDto(
                ['message' => 'Image not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param UpdateImageValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onUpdateImageValid(UpdateImageValidEvent $event)
    {
        $this->imageManager->updateImage($event->getImage());
    }
}
