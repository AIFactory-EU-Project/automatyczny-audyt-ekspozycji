<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Event\ProductGroupManagement\AddProductGroupEvent;
use App\Event\ProductGroupManagement\AddProductGroupValidEvent;
use App\Event\ProductGroupManagement\DeleteProductGroupEvent;
use App\Event\ProductGroupManagement\DeleteProductGroupValidEvent;
use App\Event\ProductGroupManagement\UpdateProductGroupEvent;
use App\Event\ProductGroupManagement\UpdateProductGroupValidEvent;
use App\Form\ProductGroupType;
use App\Service\ProductGroupManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;

class ProductGroupManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private ProductGroupManager $productGroupManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        ProductGroupManager $productGroupManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->productGroupManager = $productGroupManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddProductGroupEvent::class => 'onAddProductGroup',
            AddProductGroupValidEvent::class => 'onAddProductGroupValid',
            UpdateProductGroupEvent::class => 'onUpdateProductGroup',
            UpdateProductGroupValidEvent::class => 'onUpdateProductGroupValid',
            DeleteProductGroupEvent::class => 'onDeleteProductGroup',
            DeleteProductGroupValidEvent::class => 'onDeleteProductGroupValid',
        ];
    }

    public function onAddProductGroup(AddProductGroupEvent $event)
    {
        $productGroup = $this->productGroupManager->getNewProductGroup($event->getSystem());

        $event->setProductGroup($productGroup);

        $form = $this->formFactory->create(ProductGroupType::class, $productGroup);
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
     * @param AddProductGroupValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onAddProductGroupValid(AddProductGroupValidEvent $event)
    {
        $this->productGroupManager->updateProductGroup($event->getProductGroup());
    }

    public function onDeleteProductGroup(DeleteProductGroupEvent $event)
    {
        $productGroup = $this->productGroupManager->getProductGroup($event->getId(), $event->getSystem());
        if (!$productGroup) {
            $response = new ResponseDataDto(
                ['message' => 'ProductGroup not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    public function onDeleteProductGroupValid(DeleteProductGroupValidEvent $event)
    {
        $this->productGroupManager->deleteProductGroup($event->getProductGroup());
    }

    public function onUpdateProductGroup(UpdateProductGroupEvent $event)
    {
        $productGroup = $this->productGroupManager->getProductGroup($event->getId(), $event->getSystem());
        $event->setProductGroup($productGroup);
        if (!$productGroup) {
            $response = new ResponseDataDto(
                ['message' => 'ProductGroup not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param UpdateProductGroupValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onUpdateProductGroupValid(UpdateProductGroupValidEvent $event)
    {
        $this->productGroupManager->updateProductGroup($event->getProductGroup());
    }
}
