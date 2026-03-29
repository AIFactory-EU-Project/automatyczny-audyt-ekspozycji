<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Event\CategoryManagement\AddCategoryEvent;
use App\Event\CategoryManagement\AddCategoryValidEvent;
use App\Event\CategoryManagement\DeleteCategoryEvent;
use App\Event\CategoryManagement\DeleteCategoryValidEvent;
use App\Event\CategoryManagement\UpdateCategoryEvent;
use App\Event\CategoryManagement\UpdateCategoryValidEvent;
use App\Form\CategoryType;
use App\Service\CategoryManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;

class CategoryManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private CategoryManager $categoryManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        CategoryManager $categoryManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->categoryManager = $categoryManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddCategoryEvent::class => 'onAddCategory',
            AddCategoryValidEvent::class => 'onAddCategoryValid',
            UpdateCategoryEvent::class => 'onUpdateCategory',
            UpdateCategoryValidEvent::class => 'onUpdateCategoryValid',
            DeleteCategoryEvent::class => 'onDeleteCategory',
            DeleteCategoryValidEvent::class => 'onDeleteCategoryValid',
        ];
    }

    public function onAddCategory(AddCategoryEvent $event)
    {
        $category = $this->categoryManager->getNewCategory($event->getSystem());
        $event->setCategory($category);

        $form = $this->formFactory->create(CategoryType::class, $category);
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
     * @param AddCategoryValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onAddCategoryValid(AddCategoryValidEvent $event)
    {
        $this->categoryManager->updateCategory($event->getCategory());
    }

    public function onDeleteCategory(DeleteCategoryEvent $event)
    {
        $category = $this->categoryManager->getCategory($event->getId(), $event->getSystem());
        $event->setCategory($category);
        if (!$category) {
            $response = new ResponseDataDto(
                ['message' => 'Category not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param DeleteCategoryValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onDeleteCategoryValid(DeleteCategoryValidEvent $event)
    {
        $this->categoryManager->deleteCategory($event->getCategory());
    }

    public function onUpdateCategory(UpdateCategoryEvent $event)
    {
        $category = $this->categoryManager->getCategory($event->getId(), $event->getSystem());
        $event->setCategory($category);
        if (!$category) {
            $response = new ResponseDataDto(
                ['message' => 'Category not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }

        $form = $this->formFactory->create(CategoryType::class, $category);
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
     * @param UpdateCategoryValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onUpdateCategoryValid(UpdateCategoryValidEvent $event)
    {
        $this->categoryManager->updateCategory($event->getCategory());
    }
}
