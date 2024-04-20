import {
    Header,
    HeaderContent,
    Icon,
    FormGroup,
    FormField,
    Form,
    Input,
    TextArea,
    Button,
    Message,
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'

export default function MyFarmAddDonkey() {
    return (
        <div>
            <Header as='h2'>
                <Icon name='plus' />
                <Icon name='sticker mule' />
                <HeaderContent>My Farm</HeaderContent>
            </Header>

            <Form>
                <FormGroup widths='equal'>
                    <FormField
                        id='form-input-control-first-name'
                        control={Input}
                        label='First name'
                        placeholder='First name'
                    />
                    <FormField
                        id='form-input-control-last-name'
                        control={Input}
                        label='Last name'
                        placeholder='Last name'
                    />
                </FormGroup>
                <FormField
                    id='form-textarea-control-opinion'
                    control={TextArea}
                    label='Opinion'
                    placeholder='Opinion'
                />
                <FormField
                    id='form-input-control-error-email'
                    control={Input}
                    label='Email'
                    placeholder='joe@schmoe.com'
                    error={{
                        content: 'Please enter a valid email address',
                        pointing: 'below',
                    }}
                />
                <FormField
                    id='form-button-control-public'
                    control={Button}
                    content='Confirm'
                    label='Label with htmlFor'
                />

                <Message
                    success
                    header='Form Completed'
                    content="You're all signed up for the newsletter"
                />
            </Form>
        </div>
    );
}