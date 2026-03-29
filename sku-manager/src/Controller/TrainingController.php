<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Entity\Training;
use App\Entity\User;
use App\Event\TrainingManagement\AddTrainingEvent;
use App\Event\TrainingManagement\AddTrainingValidEvent;
use App\Event\TrainingManagement\UpdateTrainingEvent;
use App\Event\TrainingManagement\UpdateTrainingValidEvent;
use App\Form\TrainingType;
use App\Service\TrainingManager;
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
 * Class TrainingController.
 *
 * @method User getUser()
 */
class TrainingController extends AbstractDomainController
{
    /**
     * @Rest\Get("/training/{id}")
     *
     * @SWG\Get(
     *     summary="Get neural network details",
     *     tags={"Training"},
     *     @SWG\Response(
     *          response=200,
     *          description="Neural network details",
     *          @Model(type=Training::class)
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
     * @param TrainingManager $trainingManager
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function show(int $id, TrainingManager $trainingManager): Response
    {
        $training = $trainingManager->getTraining($id, $this->getUser()->getSystem());
        if (!$training) {
            return $this->handleView(
                $this->view(
                    ['message' => 'Training not found'],
                    Response::HTTP_NOT_FOUND
                )
            );
        }

        $view = $this->view($training);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Post("/training/")
     *
     * @SWG\Post(
     *     summary="Create training",
     *     tags={"Training"},
     *     @SWG\Response(
     *          response=201,
     *          description="Created training details",
     *              @SWG\Schema(
     *                  type="array",
     *                  @SWG\Items(@Model(type=Training::class, groups={"list"}))
     *          )
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
     *     description="Training creation parameters",
     *     @Model(type=TrainingType::class)
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
        $addEvent = new AddTrainingEvent($request, $this->getUser()->getSystem());
        $eventDispatcher->dispatch($addEvent);
        if ($addEvent->getResponseData()) {
            return $this->handleEventResponseData($addEvent->getResponseData());
        }

        $addValidEvent = new AddTrainingValidEvent($request, $this->getUser()->getSystem());
        $addValidEvent->setTraining($addEvent->getTraining());

        $eventDispatcher->dispatch($addValidEvent);
        if ($addValidEvent->getResponseData()) {
            $this->handleEventResponseData($addValidEvent->getResponseData());
        }

        $view = $this->view($addValidEvent->getTraining(), Response::HTTP_CREATED);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Get("/training/")
     *
     * @SWG\Get(
     *     summary="List trainings",
     *     tags={"Training"},
     *     @SWG\Response(
     *          response=200,
     *          description="Trainings",
     *          @SWG\Schema(
     *              type="array",
     *              @SWG\Items(@Model(type=Training::class, groups={"list"}))
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
     * @param TrainingManager $trainingManager
     *
     * @return Response
     */
    public function list(TrainingManager $trainingManager): Response
    {
        $trainings = $trainingManager->getTrainings($this->getUser()->getSystem());

        $view = $this->view($trainings);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Patch("/training/{id}")
     *
     * @SWG\Patch(
     *     summary="Update training",
     *     tags={"Training"},
     *     @SWG\Response(
     *          response=200,
     *          description="Updated training details",
     *          @Model(type=Training::class)
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
     *     description="Training creation parameters",
     *     @Model(type=TrainingType::class)
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
    public function update(int $id, Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $updateEvent = new UpdateTrainingEvent($request, $this->getUser()->getSystem());
        $updateEvent->setId($id);
        $eventDispatcher->dispatch($updateEvent);
        if ($updateEvent->getResponseData()) {
            return $this->handleEventResponseData($updateEvent->getResponseData());
        }

        $updateValidEvent = new UpdateTrainingValidEvent($request, $this->getUser()->getSystem());
        $updateValidEvent->setTraining($updateEvent->getTraining());

        $eventDispatcher->dispatch($updateValidEvent);
        if ($updateValidEvent->getResponseData()) {
            $this->handleEventResponseData($updateValidEvent->getResponseData());
        }

        $view = $this->view($updateValidEvent->getTraining(), Response::HTTP_OK);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
