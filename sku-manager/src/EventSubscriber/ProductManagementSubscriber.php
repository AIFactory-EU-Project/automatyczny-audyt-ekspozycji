<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Event\ProductManagement\AddProductEvent;
use App\Event\ProductManagement\AddProductValidEvent;
use App\Event\ProductManagement\DeleteProductEvent;
use App\Event\ProductManagement\DeleteProductValidEvent;
use App\Event\ProductManagement\UpdateProductEvent;
use App\Event\ProductManagement\UpdateProductValidEvent;
use App\Form\ProductType;
use App\Service\ProductManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;

class ProductManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private ProductManager $productManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        ProductManager $productManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->productManager = $productManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddProductEvent::class => 'onAddProduct',
            AddProductValidEvent::class => 'onAddProductValid',
            UpdateProductEvent::class => 'onUpdateProduct',
            UpdateProductValidEvent::class => 'onUpdateProductValid',
            DeleteProductEvent::class => 'onDeleteProduct',
            DeleteProductValidEvent::class => 'onDeleteProductValid',
        ];
    }

    public function onAddProduct(AddProductEvent $event)
    {
        $product = $this->productManager->getNewProduct($event->getSystem());
        $event->setProduct($product);
        $form = $this->formFactory->create(ProductType::class, $product);
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
     * @param AddProductValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onAddProductValid(AddProductValidEvent $event)
    {
        $this->productManager->updateProduct($event->getProduct());
    }

    public function onDeleteProduct(DeleteProductEvent $event)
    {
        $product = $this->productManager->getProduct($event->getId(), $event->getSystem());
        if (!$product) {
            $response = new ResponseDataDto(
                ['message' => 'Product not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param DeleteProductValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onDeleteProductValid(DeleteProductValidEvent $event)
    {
        $this->productManager->deleteProduct($event->getProduct());
    }

    public function onUpdateProduct(UpdateProductEvent $event)
    {
        $product = $this->productManager->getProduct($event->getId(), $event->getSystem());
        if (!$product) {
            $response = new ResponseDataDto(
                ['message' => 'Product not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param UpdateProductValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onUpdateProductValid(UpdateProductValidEvent $event)
    {
        $this->productManager->updateProduct($event->getProduct());
    }
}
