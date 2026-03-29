<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Event\BrandManagement\AddBrandEvent;
use App\Event\BrandManagement\AddBrandValidEvent;
use App\Event\BrandManagement\DeleteBrandEvent;
use App\Event\BrandManagement\DeleteBrandValidEvent;
use App\Event\BrandManagement\UpdateBrandEvent;
use App\Event\BrandManagement\UpdateBrandValidEvent;
use App\Form\BrandType;
use App\Service\BrandManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;

class BrandManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private BrandManager $brandManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        BrandManager $brandManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->brandManager = $brandManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddBrandEvent::class => 'onAddBrand',
            AddBrandValidEvent::class => 'onAddBrandValid',
            UpdateBrandEvent::class => 'onUpdateBrand',
            UpdateBrandValidEvent::class => 'onUpdateBrandValid',
            DeleteBrandEvent::class => 'onDeleteBrand',
            DeleteBrandValidEvent::class => 'onDeleteBrandValid',
        ];
    }

    public function onAddBrand(AddBrandEvent $event)
    {
        $brand = $this->brandManager->getNewBrand($event->getSystem());
        $event->setBrand($brand);

        $form = $this->formFactory->create(BrandType::class, $brand);
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
     * @param AddBrandValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onAddBrandValid(AddBrandValidEvent $event)
    {
        $this->brandManager->updateBrand($event->getBrand());
    }

    public function onDeleteBrand(DeleteBrandEvent $event)
    {
        $brand = $this->brandManager->getBrand($event->getId(), $event->getSystem());
        $event->setBrand($brand);
        if (!$brand) {
            $response = new ResponseDataDto(
                ['message' => 'Brand not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param DeleteBrandValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onDeleteBrandValid(DeleteBrandValidEvent $event)
    {
        $this->brandManager->deleteBrand($event->getBrand());
    }

    public function onUpdateBrand(UpdateBrandEvent $event)
    {
        $brand = $this->brandManager->getBrand($event->getId(), $event->getSystem());
        $event->setBrand($brand);
        if (!$brand) {
            $response = new ResponseDataDto(
                ['message' => 'Brand not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }

        $form = $this->formFactory->create(BrandType::class, $brand);
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
     * @param UpdateBrandValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onUpdateBrandValid(UpdateBrandValidEvent $event)
    {
        $this->brandManager->updateBrand($event->getBrand());
    }
}
