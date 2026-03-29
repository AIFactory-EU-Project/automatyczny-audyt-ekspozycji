<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Entity\Category;
use App\Entity\User;
use App\Event\CategoryManagement\AddCategoryEvent;
use App\Event\CategoryManagement\AddCategoryValidEvent;
use App\Event\CategoryManagement\DeleteCategoryEvent;
use App\Event\CategoryManagement\DeleteCategoryValidEvent;
use App\Event\CategoryManagement\UpdateCategoryEvent;
use App\Event\CategoryManagement\UpdateCategoryValidEvent;
use App\Form\CategoryType;
use App\Service\CategoryManager;
use App\Validation\ErrorCodes;
use FOS\RestBundle\Context\Context;
use FOS\RestBundle\Controller\Annotations as Rest;
use Nelmio\ApiDocBundle\Annotation\Model;
use Nelmio\ApiDocBundle\Annotation\Security;
use Swagger\Annotations as SWG;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

/**
 * Class CategoryController.
 *
 * @method User getUser()
 */
class CategoryController extends AbstractDomainController
{
    /**
     * @Rest\Get("/category/")
     *
     * @SWG\Get(
     *     summary="List product categories",
     *     tags={"Category"},
     *     @SWG\Response(
     *          response=200,
     *          description="Product category",
     *          @SWG\Schema(
     *              type="array",
     *              @Model(type=Category::class, groups={"list"})
     *          )
     *      ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=409, description="Conflict errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::CONFLICT_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     * )
     *
     * @Security(name="Bearer")
     *
     * @param CategoryManager $categoryManager
     *
     * @return Response
     */
    public function list(CategoryManager $categoryManager): Response
    {
        $view = $this->view($categoryManager->getCategorys($this->getUser()->getSystem()));

        $context = new Context();
        $context->setGroups(['list']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Post("/category/")
     *
     * @SWG\Post(
     *     summary="Create category",
     *     tags={"Category"},
     *     @SWG\Response(
     *          response=201,
     *          description="Created product category details",
     *          @Model(type=Category::class)
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *              @SWG\Property(property="form", type="object")
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     * )
     *
     * @SWG\Parameter(
     *     name="data",
     *     in="body",
     *     description="Product category creation parameters",
     *     @Model(type=CategoryType::class)
     * )
     *
     * @param Request                  $request
     * @param EventDispatcherInterface $eventDispatcher
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function create(Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $addEvent = new AddCategoryEvent($request, $this->getUser()->getSystem());
        $eventDispatcher->dispatch($addEvent);
        if ($addEvent->getResponseData()) {
            return $this->handleEventResponseData($addEvent->getResponseData());
        }

        $addValidEvent = new AddCategoryValidEvent($request, $this->getUser()->getSystem());
        $addValidEvent->setCategory($addEvent->getCategory());

        $eventDispatcher->dispatch($addValidEvent);
        if ($addValidEvent->getResponseData()) {
            return $this->handleEventResponseData($addValidEvent->getResponseData());
        }

        $view = $this->view($addValidEvent->getCategory(), Response::HTTP_CREATED);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Get("/category/{id}")
     *
     * @SWG\Get(
     *     summary="Get category details",
     *     tags={"Category"},
     *     @SWG\Response(
     *          response=200,
     *          description="Category details",
     *          @Model(type=Category::class)
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=409, description="Conflict errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::CONFLICT_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @param int             $id
     * @param CategoryManager $categoryManager
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function show(int $id, CategoryManager $categoryManager): Response
    {
        $category = $categoryManager->getCategory($id, $this->getUser()->getSystem());
        if (!$category) {
            return $this->handleView(
                $this->view(
                    ['message' => 'Category not found'],
                    Response::HTTP_NOT_FOUND
                )
            );
        }

        $view = $this->view($category);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Patch("/category/{id}")
     *
     * @SWG\Patch(
     *     summary="Update category",
     *     tags={"Category"},
     *     @SWG\Response(
     *          response=200,
     *          description="Updated category details",
     *          @Model(type=Category::class)
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *              @SWG\Property(property="form", type="object")
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @SWG\Parameter(
     *     name="data",
     *     in="body",
     *     description="Product category creation parameters",
     *     @Model(type=CategoryType::class)
     * )
     *
     * @param int     $id
     * @param Request $request
     *
     * @Security(name="Bearer")
     *
     * @return Response
     */
    public function update(int $id, Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $updateEvent = new UpdateCategoryEvent($request, $this->getUser()->getSystem());
        $updateEvent->setId($id);
        $eventDispatcher->dispatch($updateEvent);
        if ($updateEvent->getResponseData()) {
            return $this->handleEventResponseData($updateEvent->getResponseData());
        }

        $updateValidEvent = new UpdateCategoryValidEvent($request, $this->getUser()->getSystem());
        $updateValidEvent->setCategory($updateEvent->getCategory());

        $eventDispatcher->dispatch($updateValidEvent);
        if ($updateValidEvent->getResponseData()) {
            return $this->handleEventResponseData($updateValidEvent->getResponseData());
        }

        $view = $this->view($updateValidEvent->getCategory(), Response::HTTP_OK);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Delete("/category/{id}")
     *
     * @SWG\Delete(
     *     summary="Delete category",
     *     tags={"Category"},
     *     @SWG\Response(
     *          response=200,
     *          description="Category deleted",
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=409, description="Conflict errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::CONFLICT_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @param int                      $id
     * @param Request                  $request
     * @param EventDispatcherInterface $eventDispatcher
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function delete(int $id, Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $deleteEvent = new DeleteCategoryEvent($request, $this->getUser()->getSystem());
        $deleteEvent->setId($id);
        $eventDispatcher->dispatch($deleteEvent);
        if ($deleteEvent->getResponseData()) {
            return $this->handleEventResponseData($deleteEvent->getResponseData());
        }

        $deleteValidEvent = new DeleteCategoryValidEvent($request, $this->getUser()->getSystem());
        $deleteValidEvent->setCategory($deleteEvent->getCategory());

        $eventDispatcher->dispatch($deleteValidEvent);
        if ($deleteValidEvent->getResponseData()) {
            $this->handleEventResponseData($deleteValidEvent->getResponseData());
        }

        $view = $this->view(['message' => 'Category deleted', Response::HTTP_OK]);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
