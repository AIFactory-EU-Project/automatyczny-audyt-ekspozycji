<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Event\TrainingManagement\AddTrainingEvent;
use App\Event\TrainingManagement\AddTrainingValidEvent;
use App\Event\TrainingManagement\UpdateTrainingEvent;
use App\Event\TrainingManagement\UpdateTrainingValidEvent;
use App\Form\TrainingType;
use App\Service\TrainingManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;

class TrainingManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private TrainingManager $trainingManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        TrainingManager $trainingManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->trainingManager = $trainingManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddTrainingEvent::class => 'onAddTraining',
            AddTrainingValidEvent::class => 'onAddTrainingValid',
            UpdateTrainingEvent::class => 'onUpdateTraining',
            UpdateTrainingValidEvent::class => 'onUpdateTrainingValid',
        ];
    }

    public function onAddTraining(AddTrainingEvent $event)
    {
        $training = $this->trainingManager->getNewTraining($event->getSystem());

        //event->set resource

        $form = $this->formFactory->create(TrainingType::class, $training);
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
     * @param AddTrainingValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onAddTrainingValid(AddTrainingValidEvent $event)
    {
        $this->trainingManager->updateTraining($event->getTraining());
    }

    /**
     * @param UpdateTrainingEvent $event
     */
    public function onUpdateTraining(UpdateTrainingEvent $event)
    {
        $training = $this->trainingManager->getTraining($event->getId(), $event->getSystem());
        if (!$training) {
            $response = new ResponseDataDto(
                ['message' => 'Training not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param UpdateTrainingValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onUpdateTrainingValid(UpdateTrainingValidEvent $event)
    {
        $this->trainingManager->updateTraining($event->getTraining());
    }
}
