<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Entity\Image;
use App\Entity\User;
use App\Event\ImageManagement\AddImageEvent;
use App\Event\ImageManagement\AddImageValidEvent;
use App\Event\ImageManagement\DeleteImageEvent;
use App\Event\ImageManagement\DeleteImageValidEvent;
use App\Event\ImageManagement\UpdateImageEvent;
use App\Event\ImageManagement\UpdateImageValidEvent;
use App\Form\ImageType;
use App\Service\ImageManager;
use App\Validation\ErrorCodes;
use Exception;
use FOS\RestBundle\Context\Context;
use FOS\RestBundle\Controller\Annotations as Rest;
use Nelmio\ApiDocBundle\Annotation\Model;
use Nelmio\ApiDocBundle\Annotation\Security;
use Swagger\Annotations as SWG;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

/**
 * Class ImageController.
 *
 * @method User getUser()
 */
class ImageController extends AbstractDomainController
{
    /**
     * @Rest\Get("/image/")
     *
     * @SWG\Get(
     *     summary="List images",
     *     tags={"Image"},
     *     @SWG\Response(
     *          response=200,
     *          description="Images",
     *          @SWG\Schema(
     *              type="array",
     *              @Model(type=Image::class, groups={"list"})
     *     )),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *          @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *          @SWG\Property(property="errors", type="array", @SWG\Items(type="string"))
     *     )),
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
     * @param ImageManager $imageManager
     *
     * @return Response
     */
    public function list(ImageManager $imageManager): Response
    {
        $view = $this->view($imageManager->getImages($this->getUser()->getSystem()));

        $context = new Context();
        $context->setGroups(['list']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Post("/image/")
     *
     * @SWG\Post(
     *     summary="Create image",
     *     tags={"Image"},
     *     @SWG\Response(
     *          response=201,
     *          description="Created image details",
     *          @Model(type=Image::class)
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
     *     description="Image creation parameters",
     *     @Model(type=ImageType::class)
     * )
     *
     * @param Request $request
     *
     * @Security(name="Bearer")
     *
     * @return Response
     *
     * @throws Exception
     */
    public function create(Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $addEvent = new AddImageEvent($request, $this->getUser()->getSystem());
        $eventDispatcher->dispatch($addEvent);
        if ($addEvent->getResponseData()) {
            return $this->handleEventResponseData($addEvent->getResponseData());
        }

        $addValidEvent = new AddImageValidEvent($request, $this->getUser()->getSystem());
        $addValidEvent->setImage($addEvent->getImage());

        $eventDispatcher->dispatch($addValidEvent);
        if ($addValidEvent->getResponseData()) {
            $this->handleEventResponseData($addValidEvent->getResponseData());
        }

        $view = $this->view($addValidEvent->getImage(), Response::HTTP_CREATED);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Get("/image/{id}")
     *
     * @SWG\Get(
     *     summary="Get image details",
     *     tags={"Image"},
     *     @SWG\Response(
     *          response=200,
     *          description="Image details",
     *          @Model(type=Image::class)
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
     * @param int          $id
     * @param ImageManager $imageManager
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function show(int $id, ImageManager $imageManager): Response
    {
        $image = $imageManager->getImage($id, $this->getUser()->getSystem());
        if (!$image) {
            return $this->handleView(
                $this->view(
                    ['message' => 'Image not found'],
                    Response::HTTP_NOT_FOUND
                )
            );
        }

        $view = $this->view($image);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Patch("/image/{id}")
     *
     * @SWG\Patch(
     *     summary="Update image",
     *     tags={"Image"},
     *     @SWG\Response(
     *          response=200,
     *          description="Updated image details",
     *          @Model(type=Image::class)
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
     *     description="Image update parameters",
     *     @Model(type=ImageType::class)
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
        $updateEvent = new UpdateImageEvent($request, $this->getUser()->getSystem());
        $updateEvent->setId($id);
        $eventDispatcher->dispatch($updateEvent);
        if ($updateEvent->getResponseData()) {
            return $this->handleEventResponseData($updateEvent->getResponseData());
        }

        $updateValidEvent = new UpdateImageValidEvent($request, $this->getUser()->getSystem());
        $updateValidEvent->setImage($updateEvent->getImage());

        $eventDispatcher->dispatch($updateValidEvent);
        if ($updateValidEvent->getResponseData()) {
            $this->handleEventResponseData($updateValidEvent->getResponseData());
        }

        $view = $this->view($updateValidEvent->getImage(), Response::HTTP_OK);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Delete("/image/{id}")
     *
     * @SWG\Delete(
     *     summary="Delete image",
     *     tags={"Image"},
     *     @SWG\Response(
     *          response=200,
     *          description="Image deleted",
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
        $deleteEvent = new DeleteImageEvent($request, $this->getUser()->getSystem());
        $deleteEvent->setId($id);
        $eventDispatcher->dispatch($deleteEvent);
        if ($deleteEvent->getResponseData()) {
            return $this->handleEventResponseData($deleteEvent->getResponseData());
        }

        $deleteValidEvent = new DeleteImageValidEvent($request, $this->getUser()->getSystem());
        $deleteValidEvent->setImage($deleteEvent->getImage());

        $eventDispatcher->dispatch($deleteValidEvent);
        if ($deleteValidEvent->getResponseData()) {
            return $this->handleEventResponseData($deleteValidEvent->getResponseData());
        }

        $view = $this->view(['message' => 'User deleted', Response::HTTP_OK]);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
