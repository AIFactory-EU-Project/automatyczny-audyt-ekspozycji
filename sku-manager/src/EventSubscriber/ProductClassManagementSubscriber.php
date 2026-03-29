<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Event\ProductClassManagement\AddProductClassEvent;
use App\Event\ProductClassManagement\AddProductClassValidEvent;
use App\Event\ProductClassManagement\DeleteProductClassEvent;
use App\Event\ProductClassManagement\DeleteProductClassValidEvent;
use App\Event\ProductClassManagement\UpdateProductClassEvent;
use App\Event\ProductClassManagement\UpdateProductClassValidEvent;
use App\Form\ProductClassType;
use App\Service\ProductClassManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;

class ProductClassManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private ProductClassManager $productClassManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        ProductClassManager $productClassManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->productClassManager = $productClassManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddProductClassEvent::class => 'onAddProductClass',
            AddProductClassValidEvent::class => 'onAddProductClassValid',
            UpdateProductClassEvent::class => 'onUpdateProductClass',
            UpdateProductClassValidEvent::class => 'onUpdateProductClassValid',
            DeleteProductClassEvent::class => 'onDeleteProductClass',
            DeleteProductClassValidEvent::class => 'onDeleteProductClassValid',
        ];
    }

    public function onAddProductClass(AddProductClassEvent $event)
    {
        $productClass = $this->productClassManager->getNewProductClass($event->getSystem());

        $event->setProductClass($productClass);

        $form = $this->formFactory->create(ProductClassType::class, $productClass);
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
     * @param AddProductClassValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onAddProductClassValid(AddProductClassValidEvent $event)
    {
        $this->productClassManager->updateProductClass($event->getProductClass());
    }

    public function onDeleteProductClass(DeleteProductClassEvent $event)
    {
        $productClass = $this->productClassManager->getProductClass($event->getId(), $event->getSystem());
        if (!$productClass) {
            $response = new ResponseDataDto(
                ['message' => 'ProductClass not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    public function onDeleteProductClassValid(DeleteProductClassValidEvent $event)
    {
        $this->productClassManager->deleteProductClass($event->getProductClass());
    }

    public function onUpdateProductClass(UpdateProductClassEvent $event)
    {
        $productClass = $this->productClassManager->getProductClass($event->getId(), $event->getSystem());
        if (!$productClass) {
            $response = new ResponseDataDto(
                ['message' => 'ProductClass not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param UpdateProductClassValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onUpdateProductClassValid(UpdateProductClassValidEvent $event)
    {
        $this->productClassManager->updateProductClass($event->getProductClass());
    }
}
